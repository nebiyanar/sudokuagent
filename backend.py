
import random
import copy
def generate_sudoku(difficulty: str):
    """
    difficulty:
        'easy'   -> daha fazla sayı açık
        'medium' -> orta
        'hard'   -> daha az sayı açık
    return:
        9x9 sudoku grid, boş hücreler -1
    """

    difficulty = difficulty.lower()

    # kaç hücre boş bırakılacak
    difficulty_map = {
        "easy": 35,
        "medium": 45,
        "hard": 55
    }
    #yoksa hata atmasın diye default 45 verdik
    empty_count = difficulty_map.get(difficulty, 45)

    # boş grid oluştur
    grid = [[-1 for _ in range(9)] for _ in range(9)]

    # önce tam çözülmüş sudoku üret
    fill_sudoku(grid)

    # sonra kopyasını alıp hücre sil
    puzzle = copy.deepcopy(grid)

    removed = 0
    while removed < empty_count:
        r = random.randint(0, 8)
        c = random.randint(0, 8)

        if puzzle[r][c] != -1:
            puzzle[r][c] = -1
            removed += 1

    return puzzle


def fill_sudoku(grid):
    #solve sudoku ile benzer backtracking algoritması ama sayıları sırayla değil random atıyoruz ki farklı çözümler üretebilelim
    empty_cell = find_empty_cell(grid)

    if empty_cell is None:
        return True

    r, c = empty_cell

    nums = list(range(1, 10))
    random.shuffle(nums)

    for num in nums:
        if is_valid(grid, num, r, c):
            grid[r][c] = num

            if fill_sudoku(grid):
                return True

            grid[r][c] = -1

    return False

#aynı satırda 1 tane o sayıdan olacak
# aynı sütunda 1 tane o sayıdan olacak
# içinde bulunduğu 3x3 gridde 1 tane o sayıda olacak ve oyun 9 tane 3x3 grid içerecek
def is_valid(grid:list, num:int,r:int,c:int):
    row_value=[x for x in grid[r]]
    col_value=[grid[x][c] for x in range(0,9) ]
    #row da var mı
    if num in row_value:
        return False
    # col da var mı
    if num in col_value:
        return False
    #hangi 3x3 de olduğunun ataması

    row_normalized= r // 3  #mesela 5.satır 4.sütun yani index olarak [4,3] 4--> 1 3---> 1 
    col_normalized = c // 3 

    row_start= row_normalized * 3
    col_start = col_normalized *3

    # tüm 3x3 gridi dolaşıp checkle
    for i in range(row_start,row_start+3):
        for j in range(col_start,col_start+3):
            if grid[i][j]==num:
                return False
            
    
    return True
   
            
#böyle loop çok dönüyor son kaldığı yer gibi bişey olabilir
# en son kaldığı row en kaldığı col gibi bişey yapıp döngüyü rahatlatmaya çalışalım
def find_empty_cell(grid, last_row: int = 0, last_col: int = 0):
    # Aramaya en son kaldığımız satırdan (last_row) başlıyoruz
    for i in range(last_row, 9):
        
        # Eğer en son kaldığımız satırdaysak, sütuna 'last_col'dan başla.
        # Eğer alt satırlara geçtiysek, sütun aramasına en baştan (0'dan) başla.
        start_col = last_col if i == last_row else 0
        
        for j in range(start_col, 9):
            if grid[i][j] == -1:
                return i, j
                
    return None

def solve_sudoku(grid,last_row:int=0,last_col: int=0):
    
    empty_cell = find_empty_cell(grid,last_row,last_col)

    if  empty_cell==None:
        return True
    
    r,c = empty_cell
    for i in range(1,10):
        if is_valid(grid,i,r,c):
            grid[r][c]=i
            if  solve_sudoku(grid,r,c):
            
                return True
        
            # reset the number
            grid[r][c]=-1

    return False


def solve_sudoku_steps(grid, last_row: int = 0, last_col: int = 0):
    empty_cell = find_empty_cell(grid, last_row, last_col)

    if empty_cell is None:
        yield ("done", None, None, None)
        return True

    r, c = empty_cell

    for num in range(1, 10):
        if is_valid(grid, num, r, c):
            grid[r][c] = num
            yield ("place", r, c, num)

            solved = yield from solve_sudoku_steps(grid, r, c)
            if solved:
                return True

            grid[r][c] = -1
            yield ("remove", r, c, -1)

    return False


def get_candidates(grid, r: int, c: int):
    if grid[r][c] != -1:
        return []

    candidates = []
    for num in range(1, 10):
        if is_valid(grid, num, r, c):
            candidates.append(num)
    return candidates


def find_empty_cell_mrv(grid):
    best_cell = None
    best_candidates = None

    for r in range(9):
        for c in range(9):
            if grid[r][c] == -1:
                candidates = get_candidates(grid, r, c)

                # Bu hucre icin hic aday yoksa dal hemen basarisiz.
                if len(candidates) == 0:
                    return (r, c), []

                if best_cell is None or len(candidates) < len(best_candidates):
                    best_cell = (r, c)
                    best_candidates = candidates

                    # MRV icin teorik en iyi deger 1 oldugundan erken cikabiliriz.
                    if len(best_candidates) == 1:
                        return best_cell, best_candidates

    if best_cell is None:
        return None, []

    return best_cell, best_candidates


def solve_sudoku_mrv(grid):
    cell, candidates = find_empty_cell_mrv(grid)

    if cell is None:
        return True

    r, c = cell
    if len(candidates) == 0:
        return False

    for num in candidates:
        grid[r][c] = num

        if solve_sudoku_mrv(grid):
            return True

        grid[r][c] = -1

    return False


def solve_sudoku_steps_mrv(grid):
    cell, candidates = find_empty_cell_mrv(grid)

    if cell is None:
        yield ("done", None, None, None)
        return True

    r, c = cell
    if len(candidates) == 0:
        return False

    for num in candidates:
        grid[r][c] = num
        yield ("place", r, c, num)

        solved = yield from solve_sudoku_steps_mrv(grid)
        if solved:
            return True

        grid[r][c] = -1
        yield ("remove", r, c, -1)

    return False


def print_grid(grid):
    for i in range(9):
        # Her 3 satırda bir araya yatay ayırıcı çizgi çek (en üst hariç)
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
            
        for j in range(9):
            # Her 3 sütunda bir araya dikey ayırıcı çizgi çek (en sol hariç)
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
                
            # Satırın sonuna geldiysek alt satıra geçmek için normal print() kullan
            if j == 8:
                if grid[i][j] == -1:
                    print(".")
                else:
                    print(grid[i][j])
            else:
                # -1'leri nokta olarak yazdır, sayıları normal yazdır
                if grid[i][j] == -1:
                    print(". ", end="")
                else:
                    print(f"{grid[i][j]} ", end="")



