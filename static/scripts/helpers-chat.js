
// append newMsg to logs View
export function addMsg(contText, msgPos, msgOriginator, parrentToAapped = 'msg-area') {
  let msgSlot = document.createElement('div');
  msgSlot.className = 'message-in';
    let msgContainer = document.createElement('div');
    msgContainer.className = msgPos;
      let msgContent = document.createElement('div');
      msgContent.className = msgOriginator;
      msgContent.innerText = contText;
    
      msgContainer.appendChild(msgContent);
  msgSlot.appendChild(msgContainer);
  document.getElementById(parrentToAapped).appendChild(msgSlot);
  scrollDownlogsWindow();
};

// Scroll chat window down
export function scrollDownlogsWindow(scrollBox = ".msg") {
  const logsWindow = document.querySelector(scrollBox);
  logsWindow.scrollTop = logsWindow.scrollHeight;
};