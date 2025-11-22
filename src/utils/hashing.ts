import CryptoJS from 'crypto-js';

export const sha256 = (text: string): string => {
  return CryptoJS.SHA256(text).toString(CryptoJS.enc.Hex);
};

export const hashUrl = (url: string): string => {
  return sha256(url);
};

export const hashOwner = (email: string): string => {
  return sha256(email);
};