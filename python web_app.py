from flask import Flask, render_template, request, jsonify
import hashlib
import requests
import logging
from src.gofile_utils import get_content_id, generate_content_url, get_account_token
from src.config import BASE_HEADERS, GOFILE_API

app = Flask(__name__)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoFileWebExtractor:
    """从GoFile URL提取真实下载链接的类"""
    
    def __init__(self):
        self.token = get_account_token()
    
    def _prepare_headers(self, include_auth=False):
        """准备HTTP请求头"""
        headers = BASE_HEADERS.copy()
        
        if include_auth:
            headers["Authorization"] = f"Bearer {self.token}"
        else:
            headers["Cookie"] = f"accountToken={self.token}"
            
        return headers
    
    def extract_download_links(self, url, password=None):
        """从GoFile URL提取下载链接"""
        try:
            content_id = get_content_id(url)
            if not content_id:
                return {"error": "无效的GoFile URL"}
            
            hashed_password = (
                hashlib.sha256(password.encode()).hexdigest()
                if password else None
            )
            
            content_url = generate_content_url(content_id, password=hashed_password)
            headers = self._prepare_headers(include_auth=True)
            
            response = requests.get(content_url, headers=headers, timeout=10)
            response_data = response.json()
            
            if response_data["status"] != "ok":
                return {"error": "无法从GoFile获取响应"}
            
            data = response_data["data"]
            
            # 检查是否需要密码
            if "password" in data and data.get("passwordStatus") != "passwordOk":
                return {"error": "此URL需要有效密码"}
            
            files_info = []
            self._parse_content(data, files_info, password)
            
            return {"files": files_info}
            
        except Exception as e:
            logger.error(f"提取链接时出错: {str(e)}")
            return {"error": f"提取链接时出错: {str(e)}"}
    
    def _parse_content(self, data, files_info, password=None):
        """解析内容并提取文件信息"""
        if data["type"] == "folder":
            # 处理文件夹
            for child_id in data["children"]:
                child = data["children"][child_id]
                if child["type"] == "folder":
                    # 递归处理子文件夹
                    self._parse_content(child, files_info, password)
                else:
                    # 添加文件信息
                    files_info.append({
                        "filename": child["name"],
                        "download_link": child["link"],
                        "size": child.get("size", "未知")
                    })
        else:
            # 处理单个文件
            files_info.append({
                "filename": data["name"],
                "download_link": data["link"],
                "size": data.get("size", "未知")
            })

@app.route('/')
def index():
    """主页面"""
    return render_template('index.html')

@app.route('/extract_links', methods=['POST'])
def extract_links():
    """提取下载链接的API端点"""
    try:
        data = request.get_json()
        urls = data.get('urls', [])
        password = data.get('password', None)
        
        extractor = GoFileWebExtractor()
        results = []
        
        for url in urls:
            url_result = {
                "url": url,
                "files": [],
                "error": None
            }
            
            extraction_result = extractor.extract_download_links(url.strip(), password)
            
            if "error" in extraction_result:
                url_result["error"] = extraction_result["error"]
            else:
                url_result["files"] = extraction_result["files"]
                
            results.append(url_result)
        
        return jsonify({"results": results})
        
    except Exception as e:
        logger.error(f"处理请求时出错: {str(e)}")
        return jsonify({"error": f"处理请求时出错: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
