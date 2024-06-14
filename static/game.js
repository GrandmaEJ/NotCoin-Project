document.getElementById('tapButton').addEventListener('click', function() {
    fetch('/api/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: userId,
            action: 'tap'
        })
    }).then(response => response.json())
      .then(data => {
          document.getElementById('coinCount').innerText = data.coins;
      });
});
