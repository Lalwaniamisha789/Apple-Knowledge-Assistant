import math

def simple_calculator(query: str) -> str:
    try:
        return str(eval(query, {"__builtins__": {}}, vars(math)))
    except Exception as e:
        return f"Calculation error: {e}"

def simple_define(term: str) -> str:
    definitions = {
        "RAM": "RAM (Random Access Memory) is temporary memory used to store data that is being processed.",
        "CPU": "CPU (Central Processing Unit) is the main processor that performs calculations and runs programs.",
        "IPHONE": "iPhone is Apple's flagship smartphone series known for its performance, design, and camera quality.",
        "IPAD": "iPad is Apple's tablet line offering touchscreen computing for productivity, media, and drawing.",
        "MACBOOK": "MacBook is Apple's laptop series, including Air (lightweight) and Pro (performance-focused) models.",
        "APPLE WATCH": "Apple Watch is a smartwatch by Apple for health tracking, notifications, and fitness.",
        "AIRPODS": "AirPods are wireless Bluetooth earbuds by Apple with models including Pro (with ANC) and Max (over-ear).",
        "HOMEPOD": "HomePod is Apple’s smart speaker line designed for high-quality audio and Siri-based smart home control.",
        "M1": "M1 is Apple's first-generation silicon chip for MacBooks and iPads, providing high performance and efficiency.",
        "M2": "M2 is the second-generation chip, offering improvements in CPU, GPU, and AI performance over M1.",
        "M3": "M3 chip improves graphics and machine learning even further, used in newer MacBooks.",
        "M4": "M4 is the latest Apple silicon chip as of 2024, offering top-tier performance and efficiency."
    }

    return definitions.get(term.strip().upper(), "Definition not found.")

def compare_specs(query: str) -> str:
    q = query.lower()

    if "macbook air" in q and "macbook pro" in q:
        return (
            "MacBook Air: Lightweight, fanless, long battery life, ideal for students and basic tasks.\n"
            "MacBook Pro: Heavier, includes active cooling and better performance (M4 Pro/Max), ideal for professionals."
        )
    
    if "ipad pro" in q and "ipad air" in q:
        return (
            "iPad Pro: Higher-end with M4 chip, better display (OLED), supports Apple Pencil Pro and Magic Keyboard.\n"
            "iPad Air: More affordable, with M2 chip and Liquid Retina display, also supports Pencil and Keyboard."
        )
    
    if "m3" in q and "m4" in q:
        return (
            "M4: Newest chip with enhanced efficiency, better AI and GPU performance.\n"
            "M3: Slightly older, still very capable but less powerful in graphics and AI tasks."
        )

    if "iphone 14" in q and "iphone 15" in q:
        return (
            "iPhone 15: Newer A17 chip, USB-C port, better camera features.\n"
            "iPhone 14: Slightly older A15/A16 chip, Lightning port, still excellent performance."
        )

    return "Comparison details not available. Please specify two Apple models or chips to compare."
