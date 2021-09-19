const Twit = require('twit')
const notifier = require('node-notifier')
const apen = require('open')
const franc = require('franc')

//Aqui van las credenciales de la cuenta developer, cambiar por las propias
const apiKey = ''
const apiSecretKey = ''
const accessToken = ''
const accessTokenSecret

var T = new Twit({
    consumer_key:           apiKey,
    consumer_secret:        apiSecretKey,
    access_token:           accessToken,
    access_token_secret:    accessTokenSecret,
});

(async () => {
    //Funcion para buscar los tweets recientes
    T.get('search/tweets', { q: '#xiaomi since:2021-09-15', count: 10000 }), function(err, data, response){
        const tweets = data
        console.log(tweets)
    }
    //Funcion de streaming para obtener datos mientras ejecuta la app
})