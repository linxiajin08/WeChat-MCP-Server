#!/usr/bin/env python3
"""
微信控制器
处理微信自动化发送消息功能。
"""

import asyncio
import time
import threading
import logging
from typing import Optional, Tuple
import pyautogui
import win32gui
import win32con


class WeChatController:
    """微信自动化操作控制器。"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # 配置 pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
    
    def _find_wechat_window(self) -> Optional[int]:
        """查找微信主窗口句柄。"""
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if "微信" in window_text or "WeChat" in window_text:
                    windows.append(hwnd)
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        if windows:
            self.logger.info(f"Found WeChat window: {windows[0]}")
            return windows[0]
        else:
            self.logger.error("WeChat window not found")
            return None
    
    def _activate_window(self, hwnd: int) -> bool:
        """激活窗口并将其置于前台。"""
        try:
            # 如果窗口最小化则恢复
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            # 置于前台
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.5)
            return True
        except Exception as e:
            self.logger.error(f"Failed to activate window: {e}")
            return False
    
    def _search_contact(self, contact_name: str) -> bool:
        """在微信中搜索联系人。"""
        try:
            # 使用 Ctrl+F 打开搜索
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(0.5)
            
            # 清空搜索框并输入联系人姓名
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.typewrite(contact_name)
            time.sleep(1)
            
            # 按回车键搜索
            pyautogui.press('enter')
            time.sleep(1)
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to search contact {contact_name}: {e}")
            return False
    
    def _send_text(self, message: str) -> bool:
        """在当前聊天中发送文本消息。"""
        try:
            # 输入消息
            pyautogui.typewrite(message)
            time.sleep(0.5)
            
            # 按回车键发送
            pyautogui.press('enter')
            time.sleep(0.5)
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to send text: {e}")
            return False
    
    async def send_text_message(self, contact_name: str, message: str) -> bool:
        """向指定联系人发送文本消息。"""
        try:
            self.logger.info(f"Sending message to {contact_name}: {message}")
            
            # 查找并激活微信窗口
            wechat_hwnd = self._find_wechat_window()
            if not wechat_hwnd:
                return False
            
            if not self._activate_window(wechat_hwnd):
                return False
            
            # 搜索联系人
            if not self._search_contact(contact_name):
                return False
            
            # 发送消息
            if not self._send_text(message):
                return False
            
            self.logger.info(f"Successfully sent message to {contact_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            return False
    
    async def schedule_message(self, contact_name: str, message: str, delay_seconds: float) -> bool:
        """安排在延迟后发送消息。"""
        try:
            self.logger.info(f"Scheduling message to {contact_name} in {delay_seconds} seconds")
            
            def delayed_send():
                time.sleep(delay_seconds)
                # 在新的事件循环中运行异步函数
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    result = loop.run_until_complete(self.send_text_message(contact_name, message))
                    self.logger.info(f"Scheduled message sent successfully: {result}")
                finally:
                    loop.close()
            
            # 在单独的线程中启动延迟发送
            thread = threading.Thread(target=delayed_send, daemon=True)
            thread.start()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error scheduling message: {e}")
            return False
    
    def get_status(self) -> dict:
        """获取微信控制器的当前状态。"""
        wechat_hwnd = self._find_wechat_window()
        return {
            "wechat_available": wechat_hwnd is not None,
            "window_handle": wechat_hwnd
        }