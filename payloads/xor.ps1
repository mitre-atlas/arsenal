$enc = [System.Text.Encoding]::UTF8

function xor {
    param($string, $method)
    $xorkey = $enc.GetBytes("password123")

    if ($method -eq "decrypt"){
        $string = $enc.GetString([System.Convert]::FromBase64String($string))
    }

    $byteString = $enc.GetBytes($string)
    $xordData = $(for ($i = 0; $i -lt $byteString.length; ) {
        for ($j = 0; $j -lt $xorkey.length; $j++) {
            $byteString[$i] -bxor $xorkey[$j]
            $i++
            if ($i -ge $byteString.Length) {
                $j = $xorkey.length
            }
        }
    })

    if ($method -eq "encrypt") {
        $xordData = [System.Convert]::ToBase64String($xordData)
    } else {
        $xordData = $enc.GetString($xordData)
    }

    return $xordData
}

$FullName=$args[0]
$Contents = (cat $FullName)
if($Contents) {
    $output = xor $Contents "encrypt"
    $output > ($FullName + '.enc')
}
