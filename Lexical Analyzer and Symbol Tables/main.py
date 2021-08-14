from scanner import Scanner

def main():
   scanner = Scanner()
   
   with open('sample.mgol') as f:
        while True: # TODO: melhorar leitura
            char = f.read(1) if char else '$'
            token = scanner.scan(text)
        
            if char == '$':
                break


if __name__ == '__main__':
    main()
