/*
format datetime
 */
function pluralize (time, label) {
  if (time === 1) {
    return time + label
  }
  return time + label + 's'
}

export function timeAgo (time) {
  const between = Date.now() / 1000 - Number(time)
  if (between < 3600) {
    return pluralize(~~(between / 60), ' minute')
  } else if (between < 86400) {
    return pluralize(~~(between / 3600), ' hour')
  } else {
    return pluralize(~~(between / 86400), ' day')
  }
}

export function parseTime (time, cFormat) {
  if (arguments.length === 0) {
    return null
  }

  if ((time + '').length === 10) {
    time = +time * 1000
  }

  const format = cFormat || '{y}-{m}-{d} {h}:{i}:{s}'
  let date
  if (typeof time === 'object') {
    date = time
  } else {
    date = new Date(parseInt(time))
  }
  const formatObj = {
    y: date.getFullYear(),
    m: date.getMonth() + 1,
    d: date.getDate(),
    h: date.getHours(),
    i: date.getMinutes(),
    s: date.getSeconds(),
    a: date.getDay()
  }
  const timeStr = format.replace(/{(y|m|d|h|i|s|a)+}/g, (result, key) => {
    let value = formatObj[key]
    if (key === 'a') return ['一', '二', '三', '四', '五', '六', '日'][value - 1]
    if (result.length > 0 && value < 10) {
      value = '0' + value
    }
    return value || 0
  })
  return timeStr
}

export function formatTime (time, option) {
  time = +time * 1000
  const d = new Date(time)
  const now = Date.now()

  const diff = (now - d) / 1000

  if (diff < 30) {
    return '刚刚'
  } else if (diff < 3600) { // less 1 hour
    return Math.ceil(diff / 60) + '分钟前'
  } else if (diff < 3600 * 24) {
    return Math.ceil(diff / 3600) + '小时前'
  } else if (diff < 3600 * 24 * 2) {
    return '1天前'
  }
  if (option) {
    return parseTime(time, option)
  } else {
    return d.getMonth() + 1 + '月' + d.getDate() + '日' + d.getHours() + '时' + d.getMinutes() + '分'
  }
}

/* 数字 格式化 */
export function nFormatter (num, digits) {
  const si = [
    { value: 1E18, symbol: 'E' },
    { value: 1E15, symbol: 'P' },
    { value: 1E12, symbol: 'T' },
    { value: 1E9, symbol: 'G' },
    { value: 1E6, symbol: 'M' },
    { value: 1E3, symbol: 'k' }
  ]
  for (let i = 0; i < si.length; i++) {
    if (num >= si[i].value) {
      return (num / si[i].value + 0.1).toFixed(digits).replace(/\.0+$|(\.[0-9]*[1-9])0+$/, '$1') + si[i].symbol
    }
  }
  return num.toString()
}

export function html2Text (val) {
  const div = document.createElement('div')
  div.innerHTML = val
  return div.textContent || div.innerText
}

export function toThousandslsFilter (num) {
  return (+num || 0).toString().replace(/^-?\d+/g, m => m.replace(/(?=(?!\b)(\d{3})+$)/g, ','))
}

// 保留小数
export function toFixFun (value, num) {
  return parseInt(value).toFixed(num)
}

// 逗号分隔数字
export function formatNum (value, num) {
  num = num > 0 && num <= 20 ? num : 0
  value = parseFloat((value + '').replace(/[^\d.-]/g, '')).toFixed(num) + ''
  let l = value.split('.')[0].split('').reverse()
  let r = value.split('.')[1]
  // console.log(typeof r)
  let t = ''
  for (let i = 0; i < l.length; i++) {
    t += l[i] + ((i + 1) % 3 === 0 && (i + 1) !== l.length ? ',' : '')
  }
  return t.split('').reverse().join('') + '.' + r
}

// 人民币转换
export function cnyFun (value, rate, num) {
  let rateNum = (parseInt(value) * rate).toFixed(num).toString()
  let len = rateNum.length
  if (len <= 3) {
    return rateNum
  } else {
    let r = len % 3
    if (rateNum.slice(r, len).match(/\d{3}/g) === null) {
      return
    }
    return r > 0 ? rateNum.slice(0, r) + ',' + rateNum.slice(r, len).match(/\d{3}/g).join(',') : rateNum.slice(r, len).match(/\d{3}/g).join(',')
  }
}

// 比特币转换
export function bitcoinFun (value, rate, num) {
  let rateNum = (parseInt(value) * rate).toFixed(num).toString()
  let len = rateNum.length
  if (len <= 3) {
    return rateNum
  } else {
    let r = len % 3
    return r > 0 ? rateNum.slice(0, r) + ',' + rateNum.slice(r, len).match(/\d{3}/g).join(',') : rateNum.slice(r, len).match(/\d{3}/g).join(',')
  }
}
