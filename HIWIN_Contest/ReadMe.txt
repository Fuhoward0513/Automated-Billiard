使用State Machine 功能:

至 C 槽創建 SM_ON_OFF_FILE.txt / HIWIN ROBOT NC CODE .txt 兩個檔案

當 SM_ON_OFF_FILE.txt 內容為 1 時，手臂執行  HIWIN ROBOT NC CODE .txt 指令


指令格式(可參閱 HIWIN ROBOT NC CODE .txt):

MOVE	L	X 200	Y 450	Z 120	A 180	B 0	C 90	F 100

->(MOVE)移動 + TAB鍵 + (L)直線運動 + (位置)X + 空白鍵 + (位置)Y + 空白鍵 + (位置)Z + 空白鍵 + (位置)A + 空白鍵 + (位置)B + 空白鍵 + (位置)C


SLEEP	1000

->SLEEP + TAB鍵 + 睡眠毫秒數

IO	17	1	1000 

->IO + TAB鍵 + DIGITAL OUTPUT 點位 + TAB鍵 + ON(1:擊球)/OFF(0:收球) + TAB鍵 + 睡眠毫秒數

