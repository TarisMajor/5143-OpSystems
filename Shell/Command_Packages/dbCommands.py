import sqlite3
from rich.text import Text
from rich import print
import base64


db_path = './P01/ApiStarter/data/filesystem.db'  

class DbCommands:
    
    def append_contents(db_path, file_name, dir_id, contents):
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get the old contents from the file
        query = """
        SELECT contents FROM files WHERE pid = ? AND name = ?;
        """        
        
        cursor.execute(query, (dir_id, file_name))
        
        old_contents = cursor.fetchone()
        old_contents = old_contents[0]
        
        decoded = base64.b64decode(old_contents)
        decoded_content = decoded.decode('utf-8')
        
        query = """
        UPDATE files
        SET contents = ?,
            modified_date = DATETIME('now')
        WHERE pid = ? AND name = ?;
        """
        contents = decoded_content + '\n' + str(contents)
        
        # Encode contents to base64
        encoded = contents.encode('utf-8')
        contents = base64.b64encode(encoded)
        
        cursor.execute(query, (contents, dir_id, file_name))
        conn.commit()
        conn.close()
        
        return(f'{file_name} was appended successfully.')
    
    def new_file(db_path, file_name, contents, pid):
        
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        contents = str(contents)
        # Get the size of the string in bytes
        size = len(contents.encode('utf-8'))
        
        # Encode contents to base64
        encoded = contents.encode('utf-8')
        contents = base64.b64encode(encoded)
        
        query = """
        
        INSERT INTO files (name, pid, oid, size, creation_date, modified_date, contents, read_permission, write_permission, execute_permission, world_read, world_write, world_execute)
        VALUES (?, ?, 1, ?, DATETIME('now'), DATETIME('now'), ?, 1, 1, 0, 0, 0, 0)
        """
        
        cursor.execute(query, (file_name, pid, size, contents))
        conn.commit()
        conn.close()
        return('Completed.')
    
    def move(db_path, file1, file2, file2_pid):
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        query = """
        
        UPDATE files
        SET name = ?, pid = ?, modified_date = DATETIME('now')
        WHERE name = ?
        
        """
        
        cursor.execute(query, (file2, file2_pid, file1))
        conn.commit()
        conn.close()
        
        return('Move Successful.')
        
    
    def copy(db_path, copy_file, paste_file, paste_pid):
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        query = """
        SELECT size, contents
        FROM files
        WHERE name = ?
        """

        # Query to check if the file exists
        cursor.execute(query, (copy_file,))
        
        file_contents = cursor.fetchone()
        
        size, contents = file_contents
        
        query = """
        INSERT INTO files (pid, name, size, contents, oid, creation_date, modified_date, read_permission, write_permission, execute_permission, world_read, world_write, world_execute)
        VALUES (?, ?, ?, ?, 1, DATETIME('now'), DATETIME('now'), 1, 1, 0, 0, 0, 0)
        """
        cursor.execute(query, (paste_pid, paste_file, size, contents),)
        conn.commit()
        conn.close()
        
        return('Copy Successful.')

    def get_Content(db_path, file_id, dir_id):
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to check if the file exists
        cursor.execute(f'SELECT contents FROM files WHERE id = "{file_id}" AND pid = "{dir_id}"')
        content = cursor.fetchone()
        
        content = b''.join(content)
        content = base64.b64decode(content)
        content = content.decode("utf-8")
            
        # Close the connection
        cursor.close()
        conn.close()
        return content
    
    def get_dir_id(db_path, name):
        """
        Gets directory id in the SQLite database.

        Parameters:
            db_path (str): Path to the SQLite database.
            name (str): Name of the directory to search for.

        Returns:
            int: Directory ID
        """
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
            
        cursor.execute("SELECT id FROM directories WHERE name=?", (name,))
        dir_id = cursor.fetchone()
    
        did = int
        # Fetch the result
    
        for id in dir_id:
            did = id

        # Close the connection
        cursor.close()
        conn.close()
        
        return did
        
    def change_permissions(db_path, name, new_permissions):
         # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        digit_list = [int(digit) for digit in str(new_permissions)]
        
        reg_permissions = digit_list[0]
       
        world_permissions = digit_list[1]
        
        binary_reg = bin(reg_permissions)[2:].zfill(3)
        
        binary_world = bin(world_permissions)[2:].zfill(3)
        
        rp = binary_reg[0]
        wp = binary_reg[1]
        xp = binary_reg[2]
        
        wrp = binary_world[0]
        wwp = binary_world[1]
        wxp = binary_world[2]
        
        r_query = """
        UPDATE files
        SET read_permission = ?,
            write_permission = ?,
            execute_permission = ?
        WHERE name = ?
        """
        
        world_query = """
        UPDATE files
        SET world_read = ?,
            world_write = ?,
            world_execute = ?
        WHERE name = ?
        """

        # Query to check if the file exists
        cursor.execute(r_query, (rp, wp, xp, name))
        cursor.execute(world_query, (wrp, wwp, wxp, name))
        conn.commit()
        conn.close()
        
        return(f"Change Successful.")
    
    def get_file_and_dir_id(db_path, name):
        """
        Check if a file exists in the SQLite database.

        Parameters:
            db_path (str): Path to the SQLite database.
            file_name (str): Name of the file to search for.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to check if the file exists
        cursor.execute("SELECT id FROM files WHERE name=?", (name,))
        file_id = cursor.fetchone()
    
        cursor.execute("SELECT pid FROM files WHERE name=?", (name,))
        dir_id = cursor.fetchone()
    
        fid = int
        did = int
        # Fetch the result
    
    
        for id in file_id:
            fid = id
        
        for id in dir_id:
            did = id

        # Close the connection
        cursor.close()
        conn.close()

        return [fid, did]
    
    def file_exists(db_path, name, dir_id):
        """
        Check if a file exists in the SQLite database.

        Parameters:
            db_path (str): Path to the SQLite database.
            file_name (str): Name of the file to search for.
            dir_id (int): Directory ID of the parent folder

        Returns:
            bool: True if the file exists, False otherwise.
        """
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print('got into exists')
        
        name = str(name)
        dir_id = str(dir_id)
        print(f'name = {name} and pid = {dir_id}')
        
        query = """
            SELECT EXISTS (SELECT 1 FROM files WHERE name = ? AND pid = ?);
        """

        # Query to check if the file exists
        cursor.execute(query, (name, dir_id))
    
        # Fetch the result
        exists = cursor.fetchone()[0] == 1   # returns True if exists, False otherwise
        print(exists)
        conn.close()

        return bool(exists)

    def dir_exists(db_path, name):
        """
        Check if a file exists in the SQLite database.

        Parameters:
            db_path (str): Path to the SQLite database.
            file_name (str): Name of the file to search for.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to check if the file exists
        cursor.execute("SELECT EXISTS(SELECT 1 FROM directories WHERE name=?)", (name,))
    
        # Fetch the result
        exists = cursor.fetchone()[0] == 1  # returns True if exists, False otherwise

        return exists

    def get_listing(db_path, dir_id):
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to check if the file exists
        cursor.execute(f'SELECT name FROM files WHERE  pid = "{dir_id}"')
        files = cursor.fetchall()
        
        files = [file[0] for file in files]
        
        files = "\t".join(files)
        
        # Query to check if the file exists
        cursor.execute(f'SELECT name FROM directories WHERE pid = "{dir_id}"')
        directories = cursor.fetchall()
        
        directories = [directory[0] for directory in directories]
        
        directories = "\t".join(directories)

        directories = Text(directories)
        files = Text(files)
        directories.stylize("cyan")
        files.stylize("white")
        
        listing = directories + "\n" + files
                
        return listing
    
    
    
    def get_long_listing(db_path, dir_id, flags):
         # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query to check if the file exists
        cursor.execute(f'SELECT name FROM files WHERE  pid = "{dir_id}"')
        file_names = cursor.fetchall()
        file_names = list(file_names)
        
         # Query to check if the file exists
        cursor.execute(f'SELECT name FROM directories WHERE pid = "{dir_id}"')
        directory_names = cursor.fetchall()
        
        file_names = [name[0] for name in file_names]
        directory_names = [directory[0] for directory in directory_names]
        
        table = []
        
        for name in directory_names:
            
            temp_table = []
            # Gets the directory permissions
            cursor.execute('SELECT read_permission, write_permission, execute_permission, world_read, world_write, world_execute FROM directories WHERE name = ?', (name,))
            directory_permissions = cursor.fetchone()
            
            directory_permissions = list(directory_permissions)
            temp_perm = 'd'
            
            # Iterate over each character in the input string
            for index, char in enumerate(directory_permissions):
                if index % 3 == 0:  # Positions 0, 3, 6, ... get 'r'
                    if char == 1:
                        temp_perm += 'r'
                    else:
                        temp_perm += '-'
                elif index % 3 == 1:  # Positions 1, 4, 7, ... get 'w'
                    if char == 1:
                        temp_perm += 'w'
                    else:
                        temp_perm += '-'
                elif index % 3 == 2:  # Positions 2, 5, 8, ... get 'x'
                    if char == 1:
                        temp_perm += 'x'
                    else:
                        temp_perm += '-'
            directory_permissions = temp_perm
            
            # Default directory size
            directory_size = 4096
            
            if 'h' in flags:
                if directory_size >= 1000:
                    directory_size =  f"{directory_size / 1000:.1f}k"
                str(directory_size)
            else: 
                directory_size = str(directory_size)
            
            cursor.execute(f'Select created_at, modified_at FROM directories WHERE name = ?', (name,))
            directory_dates = cursor.fetchone()
            directory_dates = list(directory_dates)
            
            if 'l' in flags:                        
                temp_table.insert(len(temp_table), directory_permissions)
                temp_table.insert(len(temp_table), directory_size)
                temp_table.extend(directory_dates)
            temp_table.insert(len(temp_table), name)
            
            table.append(temp_table)
        
        
        for name in file_names:
            
            temp_table = []
            # Gets the file permissions
            cursor.execute('SELECT read_permission, write_permission, execute_permission, world_read, world_write, world_execute FROM files WHERE name = ?', (name,))
            file_permissions = cursor.fetchone()
            # file_permissions = ''.join(map(str, file_permissions))
            file_permissions = list(file_permissions)
            temp_perm = '-'
            
            # Iterate over each character in the input string
            for index, char in enumerate(file_permissions):
                if index % 3 == 0:  # Positions 0, 3, 6, ... get 'r'
                    if char == 1:
                        temp_perm += 'r'
                    else:
                        temp_perm += '-'
                elif index % 3 == 1:  # Positions 1, 4, 7, ... get 'w'
                    if char == 1:
                        temp_perm += 'w'
                    else:
                        temp_perm += '-'
                elif index % 3 == 2:  # Positions 2, 5, 8, ... get 'x'
                    if char == 1:
                        temp_perm += 'x'
                    else:
                        temp_perm += '-'
            file_permissions = temp_perm
            
            # Gets the file size
            cursor.execute(f'SELECT size FROM files WHERE name = ?', (name,))
            file_size = cursor.fetchone()
            
            if 'h' in flags:
                file_size = int(''.join(map(str, file_size)))
                
                if file_size >= 1000:
                    file_size =  f"{file_size / 1000:.1f}k"
                str(file_size)
            else:
                file_size = ''.join(map(str, file_size))
            
            cursor.execute(f'Select creation_date, modified_date FROM files WHERE name = ?', (name,))
            file_dates = cursor.fetchone()
            file_dates = list(file_dates)
            #file_dates = [item for tup in file_dates for item in tup]
             
            if 'l' in flags:           
                temp_table.insert(len(temp_table), file_permissions)
                temp_table.insert(len(temp_table), file_size)
                temp_table.extend(file_dates)            
            temp_table.insert(len(temp_table), name)
            table.append(temp_table)
            
        if 'l' in flags:    
            table = '\n'.join(['\t'.join(sublist) for sublist in table])
        else:
            table = '\t'.join(['\t'.join(sublist) for sublist in table])
    
        return(table)
        

        # for dir in directory_names:
        #     table.append(dir)
        # table.append("\n")
            
        # for file in files:
        #     table.append(file)
        # table.append("\n")
        # #table.add_rows(files_info)
        
        #return table
    
    def get_row_number_by_name(table, name):
        for i, row in enumerate(table.rows):
            if row[0] == name:  # Assuming the name is in the first column
                return i
        return -1  # Return -1 if the name is not found