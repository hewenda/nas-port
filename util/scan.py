import nmap
import asyncio

nm = nmap.PortScanner()

def _scan_sync(host, port):
    """同步扫描函数，在线程中执行"""

    # 执行扫描
    try:
        scan_result = nm.scan(host, port)
        print(f"Scan result: {scan_result}")
    except Exception as e:
        print(f"Scan error: {e}")
        raise e

    print(f"Scan {host} : {port}, Command line: {nm.command_line()}")

    result = []
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            for port in nm[host][proto].keys():
                if nm[host][proto][port]['state'] == 'open':
                    result.append({
                        'host': host,
                        'proto': proto,
                        'port': port,
                        'name': nm[host][proto][port].get('name')
                    })
    return result

async def scan(host, port = '11001-11100') -> list[dict]:
    """异步扫描函数，在线程中执行阻塞操作"""
    return await asyncio.to_thread(_scan_sync, host, port)