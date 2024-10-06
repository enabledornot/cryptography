using LinearAlgebra
function modf(a,b)
    return Int(round((a % b + b) % b))
end
function letterToInt(c)
    return isuppercase(c) ? UInt8(c) - UInt8('A') : UInt8(c) - UInt8('a')
end
function intToLetter(int)
    return Char(UInt8('a') + int)
end
function stringToMatrix(matrix_str,dim)
    int_ary = [parse(Int, p) for p in split(matrix_str,'.')]
    return reshape(int_ary,(dim,dim))
end
function text_to_matrix(text,dim)
    split_text = [letterToInt(c) for c in text]
    num_columns = Int(ceil(length(split_text)/dim))
    println(dim)
    println(num_columns)
    matrix_text = fill(17,(dim,num_columns))
    println(matrix_text)
    i = 0
    while i < length(split_text)
        matrix_text[(i % dim)+1, Int(floor(i / dim))+1] = split_text[i+1]
        i = i + 1
    end
    return matrix_text
end
function matrix_to_text(matrix)
    dim = size(matrix)[1]
    flat_matrix = vec(matrix)
    converted_matrix = join([intToLetter(x) for x in flat_matrix],"")
    return converted_matrix
end
function euclidean_algorithm(a,b)
    # println(string(a) * "_" * string(b))
    if a % b == 1
        return (1, -floor(a/b))
    elseif a % b == 0
        return (0,0)
    else
        f1, f2 = euclidean_algorithm(b,a%b)
        # println(" "* string(f1) * "_" * string(f2))
        return (f2, f1 - f2*floor(a/b))
    end
end

function mod_divide(A,B,mod)
    f1, f2 = euclidean_algorithm(mod,modf(A, mod))
    println(f2)
    return modf(f2 * B,mod)
end
function mod_inverse(A,mod)
    f1, f2 = euclidean_algorithm(mod,modf(A, mod))
    return f2
end
# function normalizeEncodeMatrix(matrix)
#     determinant = modf(det(matrix),26)
#     println(determinant)
#     det_inverse = mod_inverse(determinant,26)
#     while det_inverse == 0
#         println(determinant)
#         matrix[1, :] .+= 2
#         determinant = modf(det(matrix),26)
#         if determinant != 0
#             det_inverse = mod_inverse(determinant,26)
#         end
#     end
#     matrix .= matrix .* det_inverse
#     println(determinant)
#     # matrix_fixed = mod_divide.(determinant,matrix,26)
#     println(matrix)
# end
function matrixInvert(matrix)
    for (i,row) in enumerate(eachrow(matrix))
        println(row[i])
        factor = mod_inverse(row[i],26)
        println(factor)
        row = modf.(row * factor,26)
        println(row)
    end
end
function encodeAffine(plaintext,matrix_str)
    dim = Int(sqrt(length(split(matrix_str,'.'))))
    encodeMatrix = stringToMatrix(matrix_str, dim)
    determinant = modf(det(encodeMatrix),26)
    if determinant == 1
        plaintext_as_matrix = text_to_matrix(plaintext,dim)
        encoded_text_as_matrix = modf.(encodeMatrix * plaintext_as_matrix,26)
        return matrix_to_text(encoded_text_as_matrix)
    else
        println("supplied matrix with nonzero det")
    end
end
function decodeAffine(encoded_text,matrix_str)
    dim = Int(sqrt(length(split(matrix_str,'.'))))
    encodeMatrix = stringToMatrix(matrix_str,dim)
    determinant = modf(det(encodeMatrix),26)
    if determinant == 1
        encoded_text_as_matrix = text_to_matrix(encoded_text,dim)
        decoded_text_as_matrix = matrixInvert(encodeMatrix)
        println(decoded_text_as_matrix)
    else
        println("supplied matrix with nonzero det")
    end
end
# print(modf(-7,26))
# print(mod_divide(9,16,26))
action = ARGS[1]
message = ARGS[2]
matrix_str = ARGS[3]

if action == "encode"
    println("encoded message:" * encodeAffine(message,matrix_str))
elseif action == "decode"
    println("decoded message:" * decodeAffine(message,matrix_str))
else
    println("invalid action")
end