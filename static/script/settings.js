async function postTelegramData(data){
    console.log(data);
    if(data.error) return;
    await fetch("/tg_auth",{
        method: 'Post',
        headers:{
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data.id_token),
        credentials: "same-origin"
    });
}