//去除左右两端的空格
function trim(str) {
    if(str == null){
        str = "";
    }
    return str.replace(/(^\s*)|(\s*$)/g, "");
}

/**
 * 交换数组中的两个元素
 * @param array
 * @param i
 * @param j
 */
function swapArray(array, i, j){
    let temp = array[i];
    array[i] = array[j];
    array[j] = temp;
}

//去除所有空格
function removeSpace(str){
    if(str == null){
        str = "";
    }
    return str.replace(/\s/g, "");
}

/**去除Input的所有空格
 **id input的id属性
*/
function removeInputSpace(id){
    if(id == null || id == ""){
        alert("传入的id值不能为空");
    }else{
        var tempObject = document.getElementById(id);
        if(tempObject == null){
            alert("不存在id值为"+id+"的对象");
        }else{
            if(/\s/.test(tempObject.value)){
                tempObject.value = removeSpace(tempObject.value);
            }
        }
    }
}

/**
 * 在[start, end]中随机选择一个值，并返回
 * @param start 起始索引
 * @param end 结束索引
 */
function randomInRange(start, end){
    let delta = end -start + 1;
    //均匀随机出现[start, end]
    return Math.floor(Math.random() * delta) + start;
}

/**
 * 双指针，分为小于等于基准值的 基准值 大于基准值的，并返回基准值的索引
 * @param data 按data进行排序
 * @param begin [begin, end]
 * @param end [begin, end]
 * @param swap_callback 交换回调函数
 */
function partition(data, begin, end, swap_callback){
    //随机选择以恶基准值
    //let index = randomInRange(begin, end);
    //swap_callback(data, begin, index);
    let pivot = data[begin];
    //交换
    while (begin < end){
        //找到一个小于pivot的值
        while (begin < end && pivot < data[end])
            end--;
        swap_callback(data, begin, end);
        //找到第一个大于pivot的值
        while (begin < end && pivot >= data[begin])
            begin++;
        swap_callback(data, begin, end);
    }
    return begin;
}

/**
 * 快速排序
 * @param data
 * @param begin
 * @param end
 * @param swap_callback
 */
function quickSort(data, begin, end, swap_callback){
    if (begin < end){
        //使用默认函数
        if (swap_callback === undefined)
            swap_callback = swapArray;
        let middle = partition(data, begin, end, swap_callback);
        quickSort(data, begin, middle-1, swap_callback);
        quickSort(data, middle+1, end, swap_callback);
    }
}