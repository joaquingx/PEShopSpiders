export default function appendToArray(arr, toAppend){
    if(typeof toAppend == 'array'){
        toAppend = [toAppend]
    }
    return arr.concat(toAppend)
}
