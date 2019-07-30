# 说明

* 功能
    ```text
    1. 获取登录的客户端的信息.
        commaon_name    # 客户端的登录名
        remote_ip       # 客户端的IP地址
        virtual_ip      # 分配给客户端的虚拟IP地址
        send_bytes      # 发送字节数
        recv_bytes      # 接收字节数
        login_time      # 登录时间

    2. kill客户端
        依赖客户端的common_name
    ```

* openvpn启动management interface
    ```bash
    /usr/sbin/openvpn --cd /etc/openvpn/ --config server.conf --management 10.0.0.1 1195
    ```

* 使用示例
    ```
    1. 安装
    pip install pyopenvpn

    2. 使用
    import pyopenvpn

    vpn = pyopenvpn.Openvpn('10.0.0.1', 1195)

    方法:
    vpn.version()           # 获取vpn的版本
    vpn.clients()           # 获取所有在线客户端
    vpn.pid()               # 获取VPN的进程ID
    vpn.kill(common_name)   # kill掉指定的客户端
    vpn.close()             # 关闭socket
    ```