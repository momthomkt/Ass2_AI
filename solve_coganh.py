import queue
size_board = 5
class MoveCarry:
    def __init__(self, position, setOfPoint):
        self.position = position

# Hàm sao chép ma trận bàn cờ
def copyBoard(board):
    return [row[:] for row in board]

# Hàm di chuyển bàn cờ đơn giản
def tryMove(board, pace):
    x = board[pace[0][0]][pace[0][1]]
    board[pace[1][0]][pace[1][1]] = x
    board[pace[0][0]][pace[0][1]] = 0

# Hàm kiểm tra 2 điểm có gần kề nhau không
def checkNearPoint(board, pace):
    # Các tọa độ x,y không hợp lệ(lớn hơn 4 hoặc nhỏ hơn 0)
    for i in pace:
        for j in i:
            if j >= size_board or j < 0:
                return False

    # 2 điểm trùng nhau
    if pace[0] == pace[1]:
        return False
    
    # 2 điểm không sát nhau    
    if abs(pace[0][0] - pace[1][0]) > 1 or abs(pace[0][1] - pace[1][1]) > 1:
        return False
    
    # Các ô có tung độ và hoành độ không cùng thuộc số chẵn hoặc số lẻ thì không gần kề theo phương chéo được
    if pace[0][0] % 2 != pace[0][1] % 2:
        if abs(pace[0][0] -pace[1][0]) == 1 and abs(pace[0][1] -pace[1][1]) == 1:
            return False

    return True

# Hàm kiểm tra nước đi hợp lệ
def checkValidMove(board, pace):
    # Các tọa độ x,y không hợp lệ(lớn hơn 4 hoặc nhỏ hơn 0)
    for i in pace:
        for j in i:
            if j >= size_board or j < 0:
                return False

    # 2 điểm trùng nhau
    if pace[0] == pace[1]:
        return False
    
    # 2 điểm không sát nhau    
    if abs(pace[0][0] - pace[1][0]) > 1 or abs(pace[0][1] - pace[1][1]) > 1:
        return False
    
    # điểm đầu không có quân cờ, điểm cuối có quân cờ
    if board[pace[0][0]][pace[0][1]] == 0 or board[pace[1][0]][pace[1][1]] == -1 or board[pace[1][0]][pace[1][1]] == 1:
        return False
    
    # Các ô có tung độ và hoành độ không cùng thuộc số chẵn hoặc số lẻ thì không đi chéo được
    if pace[0][0] % 2 != pace[0][1] % 2:
        if abs(pace[0][0] -pace[1][0]) == 1 and abs(pace[0][1] -pace[1][1]) == 1:
            return False
    
    return True

# Hàm vicinityPoint() trả về danh sách bao gồm 3 danh sách nhỏ các điểm lân cận(gần kề) của 1 điểm(Tối đa có 8 điểm xung quanh). Trong đó:
    # Nếu điểm đó chứa quân cờ:
        # result = [M, L, E]
        # M(move) = [(a, b), (c, d),...] Danh sách các điểm có thể di chuyển đến trong 1 lượt.
        # L(league) = [(w, x), (y ,z),...] Danh sách các quân đồng minh.
        # E(enemy) = [(p, q), (r, t),...] Danh sách quân địch.
        # Tổng số tuple trong cả ba danh sách M, A, E thuộc tập {3, 4, 5, 8}
    # Nếu điểm đó đang trống:
        # result = [A, B, C]
        # A = [(a, b), (c, d),...] Danh sách các điểm trống gần kề nó
        # B = [(w, x), (y ,z),...] Danh sách các quân cờ có giá trị = 1 gần kề
        # C = [(p, q), (r, t),...] Danh sách các quân cờ có giá trị = -1 gần kề
def vicinityPoint(board, point):
    p_row = point[0]
    p_col = point[1]
    player = board[p_row][p_col]
    result = [[],[],[]]
    if board[p_row][p_col] != 1 and board[p_row][p_col] != -1:
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                # Xét 8 điểm xung quanh của điểm point trừ chính nó
                if i != 0 or j != 0:
                    if p_row + i >= 0 and p_row + i <= 4 and p_col + j >= 0 and p_col + j <= 4:
                        # Kiểm tra 2 điểm kề nhau
                        if checkNearPoint(board, ((p_row, p_col), (p_row + i, p_col + j))):
                            if board[p_row + i][p_col + j] == 0:
                                result[0].append((p_row + i, p_col + j))
                            elif board[p_row + i][p_col + j] == 1:
                                result[1].append((p_row + i, p_col + j))
                            elif board[p_row + i][p_col + j] == -1:
                                result[2].append((p_row + i, p_col + j))
    else:
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                # Xét 8 điểm xung quanh của điểm point trừ chính nó
                if i != 0 or j != 0:
                    if p_row + i >= 0 and p_row + i <= 4 and p_col + j >= 0 and p_col + j <= 4:
                        # Kiểm tra 2 điểm kề nhau
                        if checkNearPoint(board, ((p_row, p_col), (p_row + i, p_col + j))): 
                            if checkValidMove(board, (point, (p_row + i, p_col + j))) == True:
                                result[0].append((p_row + i, p_col + j))
                            elif board[p_row + i][p_col + j] == player:
                                result[1].append((p_row + i, p_col + j))
                            elif board[p_row + i][p_col + j] == -player:
                                result[2].append((p_row + i, p_col + j))
    return result
    

# Hàm trả về một list các tuple [(a,b),(b,c),...], là tập các vị trí quân cờ đối thủ bị gánh khi đi nước đi pace.
def carryPoint(board, pace):
    start_row, start_col = pace[0][0], pace[0][1]
    end_row, end_col = pace[1][0], pace[1][1]

    if board[start_row][start_col] != 1 and board[start_row][start_col] != -1:
        return False
    board_result = copyBoard(board)
    tryMove(board_result, pace)
    player = board[start_row][start_col]
    result = []

    # Các điểm gánh dọc(Các điểm không nằm trên cùng, không nằm dưới cùng bàn cờ)
    if end_row > 0 and end_row < 4:
        if board_result[end_row + 1][end_col] == board_result[end_row - 1][end_col] == -player:
            result.append((end_row + 1,end_col))
            result.append((end_row - 1,end_col))
    
    # Các điểm gánh ngang(Các điểm không nằm phải cùng, không nằm trái cùng bàn cờ)
    if end_col > 0 and end_col < 4:
        if board_result[end_row][end_col + 1] == board_result[end_row][end_col - 1] == -player:
            result.append((end_row,end_col + 1))
            result.append((end_row,end_col - 1))
    
    # Các điểm gánh chéo
    if end_row > 0 and end_row < 4 and end_col > 0 and end_col < 4 and (end_row % 2) == (end_col % 2):
        if board_result[end_row + 1][end_col + 1] == board_result[end_row - 1][end_col - 1] == -player:
            result.append((end_row + 1,end_col + 1))
            result.append((end_row - 1,end_col - 1)) 
        if board_result[end_row + 1][end_col - 1] == board_result[end_row - 1][end_col + 1] == -player:
            result.append((end_row + 1,end_col - 1))
            result.append((end_row - 1,end_col + 1))

    return result

# Hàm trả về một list các tuple [(a,b),(b,c),...], là tập các vị trí quân cờ đối thủ bị chẹt khi đi nước đi pace.
# Chú ý: Hàm này sẽ tạo một board mới rồi ăn quân bằng cách gánh trên bàn cờ mới đó(nếu có), sau đó mới xét các vị trí chẹt
def surroundPoint(board, pace):
    board_result = copyBoard(board)
    cPoint = carryPoint(board, pace)
    tryMove(board_result, pace)

    lst_points = [(end_row, end_col)]
    if cPoint != False:
        for point in cPoint:
            board_result[point[0]][point[1]] = -board_result[point[0]][point[1]]

        lst_points = lst_points + cPoint
    result = []
    start_row, start_col = pace[0][0], pace[0][1]
    end_row, end_col = pace[1][0], pace[1][1]
    # Các điểm cần xét gồm: quân cờ vừa đi(end_row, end_col), và các điểm vừa bị gánh(cPoint). Các điểm này đều có thể chẹt quân địch
    # lst_points = [(end_row, end_col)] + cPoint
    for point in lst_points:
        # Hàng đợi chứa các vị trí quân cờ địch cần duyệt
        Q = queue.Queue()
        # all_lvl, list chứa các vị trí quân cờ địch đã duyệt
        all_lvl = []
        # Với từng điểm cần xét-point ta tìm các điểm gần kề với nó
        viciPoint = vicinityPoint(board_result, point)
        # Duyệt qua danh sách các quân địch liền kề
        for enemy in viciPoint[2]:
            exist = False
            for ele in all_lvl:
                if ele == enemy:
                    exist = True
            if exist:
                continue
            Q.put(enemy)
            
            # Danh sách lưu vị trí các quân cờ địch liền kề với quân địch enemy đang xét trong vòng lặp
            lvl = []
            lvl.append(enemy)
            all_lvl.append(enemy)
            is_append = True
            while not Q.empty():
                curr_enemy = Q.get()
                # Tìm các điểm xung quanh quân địch(curr_enemy) đang xét
                viciE = vicinityPoint(board_result, curr_enemy)
                # Nếu xung quanh có chỗ trống thì không bị chẹt, break vòng lặp while và đổi is_append = False với mục đích
                # làm tín hiệu để không thêm kết quả đã duyệt vào list result
                if len(viciE[0]) > 0:
                    is_append = False
                    break
                # Sau khi không có chỗ trống, nếu không có quân đồng minh bên cạnh thì bị chẹt
                if len(viciE[1]) == 0:
                    break
                for i in range(len(viciE[1])):
                    tontai = False
                    for j in range(len(lvl)):
                        if viciE[1][i] == lvl[j]:
                            tontai = True
                    if not tontai:
                        lvl.append(viciE[1][i])
                        all_lvl.append(viciE[1][i])
                        Q.put(viciE[1][i])
            if is_append:
                for ele_lvl in lvl:
                    # Nếu kết quả trong list lvl chưa có trong list result thì mới thêm vô
                    if not (ele_lvl in result):
                        result.append(ele_lvl)
    
    return result

# Hàm trả về một tuple gồm 2 nhỏ ((a,b),(c,d)) là nước cờ vừa đi của đối thủ
def findAct(prev_board, board):
    start = ()
    end = ()
    for i in range(len(prev_board)):
        for j in range(len(prev_board[i])):
            if prev_board[i][j] == 0 and board[i][j] != 0:
                end += (i,j)
            if prev_board[i][j] != 0 and board[i][j] == 0:
                start += (i,j)
    return (start,end)

# Hàm trả về một tuple (a,b) hoặc là một tuple rỗng () là điểm bắt buộc phải đi khi đối thủ vừa tạo thế cờ mở
def checkOpen(prev_board, board, player):
    # Đầu tiên ta tìm vị trí quân cờ địch vừa đi end
    start = ()
    end = ()
    for i in range(len(prev_board)):
        for j in range(len(prev_board[i])):
            if prev_board[i][j] == 0 and board[i][j] != 0:
                end += (i,j)
            if prev_board[i][j] != 0 and board[i][j] == 0:
                start += (i,j)
                
    vicPoint = vicinityPoint(board, start)
    if len(vicPoint[1]) == 0 or len(vicPoint[2]) == 0:
        return ()

    if board[start[0] + 1][start[1]] == board[start[0] - 1][start[1]] == board[end[0]][end[1]] or board[start[0]][start[1] + 1] == board[start[0]][start[1] - 1] == board[end[0]][end[1]]:
        return start 
    if start[0] % 2 == start[1] % 2:
        if board[start[0] + 1][start[1] + 1] == board[start[0] - 1][start[1] - 1] == board[end[0]][end[1]] or board[start[0] + 1][start[1] - 1] == board[start[0] - 1][start[1] + 1] == board[end[0]][end[1]]:
            return start
    return ()


red = -1
blue = 1
    
board = [[  1,  0,  1,  0,  1],
        [   1,  1,  1,  1,  1],
        [   1, -1,  1,  0,  0],
        [  -1, -1,  0,  0,  1],
        [   0,  0,  1,  0,  1]]

board2 =[[  1,  0,  1,  0,  1],
        [   1,  1,  1,  1,  1],
        [   1, -1,  1,  0,  0],
        [  -1,  0,  0,  0,  1],
        [   0, -1,  1,  0,  1]]
# player = red
# pace = ((0,2),(1,3))
# result = checkValidMove(board, pace)
# print(result)
# if result:
#     print("carryPoint: ", carryPoint(board, pace))
#     print(surroundPoint(board, pace))
# print()
# print(findAct(board, board2))
# print(vicinityPoint(board, (0,1)))
print(checkOpen(board, board2, 1))