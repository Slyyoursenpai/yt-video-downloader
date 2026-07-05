def main():
    print("Test Input=============")
    
    url = input("Paste Youtube link here: ").strip()
    
    if not url:
        print("Error: you did not enter a link")
        return
    
    print(f"Success: The link you entered is: {url}")
    
    
if __name__ == "__main__":
    main()