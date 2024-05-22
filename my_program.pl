
val m1_rows : int := 3;
val m1_cols : int := 2;
val m2_rows : int := 2;
val m2_cols : int := 2;


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
        print_int_array(m[i], cols);
        i := i + 1;
    }
}


function main() {
    val m1 : [[int]] := get_int_matrix(m1_rows, m1_cols);
    val m2 : [[int]] := get_int_matrix(m2_rows, m2_cols);

    m1[0][0] := 1;
    m1[0][1] := 2;
    m1[1][0] := 3;
    m1[1][1] := 4;
    m1[2][0] := 5;
    m1[2][1] := 6;

    m2[0][0] := 1;
    m2[0][1] := 2;
    m2[1][0] := 3;
    m2[1][1] := 4;

    print_string("Matrix 1:");
    print_matrix(m1, m1_rows, m1_cols);
    print_string("Matrix 2:");
    print_matrix(m2, m2_rows, m2_cols);

    print_string("Matrix Product:");
    
    print_matrix(matrixProduct(m1, m2), m1_rows, m2_cols);
}