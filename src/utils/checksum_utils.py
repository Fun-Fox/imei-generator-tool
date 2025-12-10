"""
校验和计算工具函数
"""


def calculate_luhn_check_digit(digits: str) -> str:
    """
    使用Luhn算法计算校验位
    
    Args:
        digits: 需要计算校验位的数字字符串
        
    Returns:
        str: 校验位
    """
    total = 0
    for i, digit in enumerate(reversed(digits)):
        n = int(digit)
        if i % 2 == 0:  # 从右边数，偶数位（索引为0, 2, 4...）
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return str((10 - total % 10) % 10)