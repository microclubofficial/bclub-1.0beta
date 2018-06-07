import Cookies from 'js-cookie'

const TokenKey = 'b-Token'

export function getToken (tokenKey = TokenKey) {
  return Cookies.get(tokenKey)
}

export function setToken (tokenKey, token, expires = {}) {
  return Cookies.set(tokenKey, token, expires)
}

export function removeToken (tokenKey = TokenKey) {
  return Cookies.remove(tokenKey)
}

export function rememberToken (rememberToken) {
  return Cookies.get(rememberToken)
}
