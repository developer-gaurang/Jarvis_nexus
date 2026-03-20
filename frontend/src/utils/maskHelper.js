export const applyDevMask = (text) => {
     // Yeh function normal text ko 8-bit Binary code mein convert karta hai
     return text.split('').map(char => char.charCodeAt(0).toString(2).padStart(8, '0')).join(' ');
};