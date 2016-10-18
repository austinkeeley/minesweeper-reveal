minesweeper-reveal
===================

A Python script that reveals the locations of mines in winmine.exe (Minesweeper 
for Microsoft Windows). Requires winappdbg.

Start an instance of winmine.exe, then run the script and provide the PID of 
the winmine.exe process. The script will inspect the memory where the gamefield
is stored and print the locations of the mines.

    C:\>python minesweeper-reveal.py
    Minesweeper Reveal
    Enter the PID of winmine.exe: 5084
    Width is 9
    Height is 9
    
    ###########
    #.*..*....#
    #..*......#
    #..*......#
    #.........#
    #.....**..#
    #.*..*...*#
    #....*....#
    #.........#
    #.........#
    ###########
