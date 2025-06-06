from argparse import *
import os

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--input", type=str, help="The input file/dir", required=True)
    return parser.parse_args()

def fix_file(input_file, verbose=False):
    # Set the first bit of VideoFullRange to 1
    # VideoFullRange is the 10th byte of the entry
    #   meta/iprp/ipco/colr
    # 
    # Ref: https://exiftool.org/TagNames/QuickTime.html#ColorRep
    
    # Check if the input file exists
    if not os.path.isfile(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        return
    
    f = open(input_file, 'rb+')
    fytp_sz = int.from_bytes(f.read(4))
    if verbose:
        print(f"fytp_sz: {fytp_sz}")
    
    # Check magic number
    magic_number = f.read(8)
    if magic_number != b'ftypheix':
        print(f"Error: The file '{input_file}' does not have the correct magic number.")
        return
    
    f.read(fytp_sz - 12)  # Read the rest of the ftyp box
    
    
    next_box_sz = int.from_bytes(f.read(4))
    while next_box_sz != 0:
        type = f.read(4)
        next_box_sz -= 8
        if verbose:
            print(f"Box type: {type}, size: {next_box_sz}")
        if (type == b'meta'):
            f.read(4) # Skip the version and flags
            next_box_sz -= 4
            
            while next_box_sz > 0:
                meta_box_sz = int.from_bytes(f.read(4))
                next_box_sz -= meta_box_sz
                meta_box_type = f.read(4)
                meta_box_sz -= 8
                if verbose:
                    print(f"Meta box type: {meta_box_type}, size: {meta_box_sz}")
                
                if meta_box_type == b'iprp':
                    while meta_box_sz > 0:
                        iprp_box_sz = int.from_bytes(f.read(4))
                        meta_box_sz -= iprp_box_sz
                        iprp_box_type = f.read(4)
                        iprp_box_sz -= 8
                        if verbose:
                            print(f"IPRP box type: {iprp_box_type}, size: {iprp_box_sz}")
                        if iprp_box_type == b'ipco':
                            while iprp_box_sz > 0:
                                ipco_box_sz = int.from_bytes(f.read(4))
                                iprp_box_sz -= ipco_box_sz
                                ipco_box_type = f.read(4)
                                ipco_box_sz -= 8
                                if verbose:
                                    print(f"IPCO box type: {ipco_box_type}, size: {ipco_box_sz}")
                                if ipco_box_type == b'colr':
                                    f.read(10)
                                    VideoFullRange = int.from_bytes(f.read(1))
                                    f.seek(-1, os.SEEK_CUR)  # Move back one byte to overwrite
                                    if VideoFullRange >> 7 == 0:
                                        if verbose:
                                            print("VideoFullRange is 0, setting to 1")
                                        f.write(bytes([VideoFullRange|0x80]))
                                    else:
                                        if verbose:
                                            print("VideoFullRange is already set to 1")
                                    break
                                f.read(ipco_box_sz)
                            break
                        f.read(iprp_box_sz) 
                    break
                f.read(meta_box_sz)
            break
        f.read(next_box_sz)
        next_box_sz = int.from_bytes(f.read(4))
        
    f.close()

def main():
    args = parse_args()
    
    input_file_dir = args.input
    if os.path.isdir(input_file_dir):
        for root, dirs, files in os.walk(input_file_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if not file_path.endswith('.HIF'):
                    continue
                print(f"Processing file: {file_path}")
                fix_file(file_path)
    else:
        print(f"Processing file: {input_file_dir}")
        fix_file(input_file_dir)

if __name__ == "__main__":
    main()
    