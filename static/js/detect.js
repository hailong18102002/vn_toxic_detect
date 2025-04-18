function handleInputTypeChange() {
    const type = document.querySelector('input[name="inputType"]:checked').value;
    const inputText = document.getElementById('inputTextContainer');
    const voice = document.getElementById('voiceControls');
    
    if (type === 'voice') {
      inputText.style.display = 'none';
      voice.style.display = 'block';
    } else {
      voice.style.display = 'none';
      inputText.style.display = 'block';
      document.getElementById('inputField').placeholder =
        type === 'url' ? 'Vui lòng nhập đường dẫn đầu vào' : 'Vui lòng nhập văn bản đầu vào';
    }
  }
  
function showResult() {
  const inputType = document.querySelector('input[name="inputType"]:checked').value;
  const inputValue = document.getElementById('inputField')?.value || '';
  const body = {
    type: inputType,
    content: inputValue,
    url: inputType === 'url' ? inputValue : ""
  };

  fetch('/api/check', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById('textBlock').innerText = data.message;
      const bar = document.querySelector('.bar-fill');
      const label = document.querySelector('.bar-label');
      const color = data.status === 'toxic' ? 'red' : 'green';
      const text = data.status === 'toxic' ? 'Nội dung toxic' : 'Nội dung không toxic';

      bar.style.width = `${data.score}%`;
      bar.style.background = color;
      label.style.color = color;
      label.innerText = `${data.score}% - ${text}`;

      document.getElementById('resultSection').style.display = 'block';
    });
}

function resetPage() {
  document.getElementById('inputField').value = '';
  document.getElementById('resultSection').style.display = 'none';
}
function logout() {
  window.location.href = "/";
}
function goToHistory() {
  window.location.href = '/history'; 
}

