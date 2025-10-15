"""SSH执行器"""

import paramiko
import time
from typing import List, Tuple


class SSHExecutor:
    """SSH执行器主类"""
    
    def __init__(self):
        self.client = None
    
    def connect(self, host: str, port: int, username: str, password: str) -> bool:
        """
        连接到SSH服务器
        
        Args:
            host: 主机地址
            port: 端口号
            username: 用户名
            password: 密码
            
        Returns:
            bool: 连接是否成功
        """
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(host, port=port, username=username, password=password, timeout=10)
            return True
        except Exception as e:
            print(f"SSH连接失败: {str(e)}")
            return False
    
    def execute_command(self, command: str) -> Tuple[bool, str, str]:
        """
        执行单个命令
        
        Args:
            command: 要执行的命令
            
        Returns:
            Tuple[bool, str, str]: (是否成功, 标准输出, 错误输出)
        """
        if not self.client:
            return False, "", "SSH客户端未连接"
        
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            stdout_str = stdout.read().decode('utf-8')
            stderr_str = stderr.read().decode('utf-8')
            return True, stdout_str, stderr_str
        except Exception as e:
            return False, "", str(e)
    
    def execute_commands(self, commands: List[str]) -> List[Tuple[bool, str, str]]:
        """
        执行多个命令
        
        Args:
            commands: 要执行的命令列表
            
        Returns:
            List[Tuple[bool, str, str]]: 每个命令的执行结果列表
        """
        results = []
        for command in commands:
            result = self.execute_command(command)
            results.append(result)
            # 添加小延迟以避免命令执行过快
            time.sleep(0.1)
        return results
    
    def disconnect(self):
        """断开SSH连接"""
        if self.client:
            self.client.close()
            self.client = None