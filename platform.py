from platformio.platform.base import PlatformBase

class JavaplatformPlatform(PlatformBase):
    """Universal Java Platform for PlatformIO with JDK 18 and Maven support"""
    
    def is_embedded(self):
        return False
