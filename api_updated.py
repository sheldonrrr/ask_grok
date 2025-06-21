    def ask_stream(self, prompt: str, lang_code: str = 'en', return_dict: bool = False) -> str:
        """向 X.AI API 发送问题并获取回答（流式请求，适用于短文本）
        
        Args:
            prompt: 问题文本
            lang_code: 语言代码，用于获取相应的翻译文本
            return_dict: 是否返回字典类型，默认为 False 返回字符串
            
        Returns:
            Union[str, dict]: 默认返回字符串，当 return_dict=True 时返回解析后的字典
        
        Note:
            这个方法不使用流式请求，更适合处理短文本和快速响应的场景
        """
        
        # 确保 token 格式正确：
        # 1. 移除所有空白字符（包括空格、tab、换行符等）
        # 2. 移除 BOM 标记
        # 3. 处理 Bearer 前缀，确保格式正确
        # 记录原始 token
        logger.debug(f"Original token: {self.auth_token}")
        
        token = self.auth_token
        token = ''.join(token.split())  # 移除所有空白字符
        token = token.encode('utf-8').decode('utf-8-sig')  # 移除可能的 BOM
        
        # 处理 Bearer 前缀
        if token.startswith('Bearer'):
            token = token[6:]
            token = token.strip()
        token = 'Bearer ' + token
        
        # 准备请求
        headers, data = self._prepare_request(prompt)
        data["stream"] = False  # 非流式请求
        headers['Authorization'] = token  # 使用处理后的 token
        
        try:
            # 添加超时设置
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data,
                timeout=60  # 增加到60秒
            )
            
            # 处理常见错误
            if response.status_code == 400:
                error_data = response.json()
                error_message = error_data.get('error', {}).get('message', 'Bad request')
                logger.error(f"API bad request: {error_message}")
                translation = get_translation(lang_code)
                raise Exception(f"{translation.get('error_prefix', 'Error:')} {error_message}")
            
            response.raise_for_status()
            
            result = response.json()
            if result.get("choices") and result["choices"][0].get("message", {}).get("content"):
                content = result["choices"][0]["message"]["content"]
                if return_dict:
                    try:
                        import json
                        return json.loads(content)
                    except json.JSONDecodeError:
                        logger.warning("返回的内容不是有效的 JSON 格式，返回原始字符串")
                        return content
                return content
            else:
                logger.error(f"Unexpected API response format: {result}")
                translation = get_translation(lang_code)
                error_message = f"{translation.get('error_prefix', 'Error:')} {translation.get('request_failed', 'API request failed')}: Unexpected response format"
                raise Exception(error_message)
                                
        except requests.exceptions.RequestException as e:
            translation = get_translation(lang_code)
            error_message = f"{translation.get('error_prefix', 'Error:')} {translation.get('request_failed', 'API request failed')}: {str(e)}"
            logger.error(error_message)
            raise Exception(error_message)
