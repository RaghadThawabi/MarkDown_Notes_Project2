fetch('http://localhost:8000/notes/NOTE-ID/render', {
    headers: {
        'Authorization': 'Bearer TOKEN',
        'If-None-Match': '"ETAG FROM THE RENDER"'  // Paste ETag here
    }
})
.then(response => {
    console.log('Status:', response.status);
    console.log('Status Text:', response.statusText);
    console.log('Headers:', [...response.headers]);
    if (response.status === 304) {
        console.log('✅ SUCCESS! Got 304 Not Modified - ETag caching works!');
    } else {
        console.log('⚠ Got', response.status, '- Expected 304');
    }
    return response.text();
})
.then(body => {
    console.log('Body length:', body.length);
    if (body.length === 0) {
        console.log('✅ Body is empty as expected for 304!');
    }
})