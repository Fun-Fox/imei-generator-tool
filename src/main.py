"""设备信息模拟与配置执行系统主程序"""

import json
import argparse
from typing import List
from .generator.device_info_generator import DeviceInfoGenerator
from .executor.dg_command_generator import DGCommandGenerator
from .core.models import DeviceInfo
from .executor.ssh_executor import SSHExecutor


def generate_device_info_batch(count: int, model: str = None, region: str = None, carrier: str = None) -> List[DeviceInfo]:
    """
    批量生成设备信息
    
    Args:
        count: 生成数量
        model: 指定设备型号
        region: 指定区域
        carrier: 指定运营商
        
    Returns:
        List[DeviceInfo]: 设备信息列表
    """
    generator = DeviceInfoGenerator()
    device_info_list = []
    
    for _ in range(count):
        device_info = generator.generate_device_info(model, region, carrier)
        device_info_list.append(device_info)
    
    return device_info_list


def save_device_info_to_json(device_info_list: List[DeviceInfo], filename: str):
    """
    将设备信息保存为JSON文件
    
    Args:
        device_info_list: 设备信息列表
        filename: 保存的文件名
    """
    data = [device_info.to_dict() for device_info in device_info_list]
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"设备信息已保存到 {filename}")


def generate_dg_commands(device_info_list: List[DeviceInfo]) -> List[List[str]]:
    """
    生成DG命令
    
    Args:
        device_info_list: 设备信息列表
        
    Returns:
        List[List[str]]: DG命令列表的列表
    """
    command_generator = DGCommandGenerator()
    commands_list = command_generator.generate_commands_batch(device_info_list)
    
    return commands_list


def save_commands_to_file(commands_list: List[List[str]], filename: str):
    """
    将DG命令保存到文件
    
    Args:
        commands_list: DG命令列表
        filename: 保存的文件名
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for i, commands in enumerate(commands_list):
            f.write(f"# 设备 {i+1} 的DG命令\n")
            for command in commands:
                f.write(f"{command}\n")
            f.write("\n")
    
    print(f"DG命令已保存到 {filename}")


def execute_commands_via_ssh(host: str, port: int, username: str, password: str, commands_list: List[List[str]]):
    """
    通过SSH执行命令
    
    Args:
        host: SSH主机地址
        port: SSH端口
        username: 用户名
        password: 密码
        commands_list: 要执行的命令列表
    """
    executor = SSHExecutor()
    
    if not executor.connect(host, port, username, password):
        print("SSH连接失败")
        return
    
    print(f"已连接到 {host}:{port}")
    
    for i, commands in enumerate(commands_list):
        print(f"\n执行设备 {i+1} 的命令:")
        results = executor.execute_commands(commands)
        
        for j, (success, stdout, stderr) in enumerate(results):
            if success:
                print(f"  命令 {j+1}: 成功")
                if stdout.strip():
                    print(f"    输出: {stdout.strip()}")
            else:
                print(f"  命令 {j+1}: 失败 - {stderr}")
    
    executor.disconnect()
    print("SSH连接已断开")


def main():
    parser = argparse.ArgumentParser(description="设备信息模拟与配置执行系统")
    parser.add_argument("-n", "--count", type=int, default=10, help="生成设备信息的数量")
    parser.add_argument("-m", "--model", type=str,default="Samsung", help="指定设备型号")
    parser.add_argument("-r", "--region", type=str,default="China", help="指定区域（国家/地区）")
    parser.add_argument("-c", "--carrier", type=str, default="China Mobile",help="指定运营商")
    parser.add_argument("-o", "--output", type=str, default="device_info.json", help="设备信息输出文件名")
    parser.add_argument("--ssh-host", type=str, help="SSH主机地址")
    parser.add_argument("--ssh-port", type=int, default=22, help="SSH端口")
    parser.add_argument("--ssh-username", type=str, help="SSH用户名")
    parser.add_argument("--ssh-password", type=str, help="SSH密码")
    parser.add_argument("--commands-file", type=str, default="dg_commands.txt", help="DG命令输出文件名")
    
    args = parser.parse_args()
    
    # 生成设备信息
    print(f"正在生成 {args.count} 条设备信息...")
    device_info_list = generate_device_info_batch(args.count, args.model, args.region, args.carrier)
    
    # 保存设备信息到JSON文件
    save_device_info_to_json(device_info_list, args.output)
    
    # 生成DG命令
    print("正在生成DG命令...")
    commands_list = generate_dg_commands(device_info_list)
    
    # 保存DG命令到文件
    save_commands_to_file(commands_list, args.commands_file)
    
    # 如果提供了SSH信息，则执行命令
    if args.ssh_host and args.ssh_username and args.ssh_password:
        print("正在通过SSH执行命令...")
        execute_commands_via_ssh(
            args.ssh_host, 
            args.ssh_port, 
            args.ssh_username, 
            args.ssh_password, 
            commands_list
        )
    else:
        print("未提供SSH信息，跳过命令执行")
    
    # 显示生成的设备信息摘要
    print("\n生成的设备信息摘要:")
    for i, device_info in enumerate(device_info_list):
        print(f"设备 {i+1}:")
        print(f"  型号: {device_info.model}")
        print(f"  IMEI: {device_info.imei}")
        print(f"  IMSI: {device_info.imsi}")
        print(f"  区域: {device_info.region}")
        print(f"  运营商: {device_info.carrier}")
        print(f"  手机号: {device_info.phone_number}")
        print()


if __name__ == "__main__":
    main()