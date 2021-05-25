using System;
using System.Text;
using System.IO;
using System.Diagnostics;
using System.ComponentModel;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Runtime.InteropServices;

class gnaf
{
    static readonly TcpClient f = new TcpClient("127.0.0.1", 8000);

    [DllImport("test.c", EntryPoint = "c")]
    static extern void c();
    public static void Main(string[] args) {
     c(); 
    }

}