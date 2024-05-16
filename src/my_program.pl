val m1_rows : int := 3;
val m1_cols : int := 2;
val m2_rows : int := 2;
val m2_cols : int := 2;

# '%tmp_33' defined with type 'i32**' but expected 'i32*'
# %residxtmp_35 = getelementptr i32, i32* %tmp_33, i32 %tmp_34
function matrixProduct(val m1 : [[int]], val m2 : [[int]]) : [[int]]{
    val res : [[int]] := get_int_matrix(m1_rows, m2_cols);
    var m1RowIdx : int := 0;
    while  m1RowIdx < m1_rows {
        var m2ColIdx : int := 0;
        while m2ColIdx<m2_rows{
            var m2RowIdx : int := 0;
            while m2RowIdx<m2_rows {
                res[m1RowIdx][m2ColIdx] := res[m1RowIdx][m2ColIdx] + m1[m1RowIdx][m2RowIdx]*m2[m2RowIdx][m2ColIdx];
                m2RowIdx := m2RowIdx + 1;
            }
            m2ColIdx := m2ColIdx + 1;
        }
        m1RowIdx := m1RowIdx + 1;
    }
    matrixProduct := res;
}


function print_matrix(val m : [[int]], val rows : int, val cols : int){
    var i : int := 0;
    while i < rows{
        print_string("row");
        print_int(i);
        print_string("--");
        var j : int := 0;
        while j < cols{
            print_int(m[i][j]);
            j := j + 1;
        }
        i := i + 1;
        print_string("--");
    }
}


function main() {
    val m1 : [[int]] := get_int_matrix(m1_rows, m1_cols);
    val m2 : [[int]] := get_int_matrix(m2_rows, m2_cols);
    
    print_matrix(matrixProduct(m1, m2), m1_rows, m2_cols);
}
