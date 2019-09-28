if __name__ == "__main__":
    main()
import os



def main(Lines, FileName="mytext.txt", Path = "output"):
    save_file_path = os.path.join(Path,FileName)
    save_file = open(save_file_path,"w")
    for line in Lines:
        save_file.write(line + "\n")
    save_file.close()