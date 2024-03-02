const fs = require('fs');
const csv = require('csv-parser');  
const { Client } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

const client = new Client();

// Evento de QR code
client.on('qr', qr => {
    qrcode.generate(qr, { small: true });
});

// Evento de cliente pronto
client.on('ready', () => {
    console.log('Cliente está pronto!');

    // Abrir o arquivo CSV para leitura
    fs.createReadStream(`C:\\Users\\tomie\\OneDrive\\Documentos\\salao\\whatsapp\\planilha_tratada\\agendamentos.csv`)

        .pipe(csv())
        .on('data', (row) => {
            // Construir a mensagem
            let mensagem = `Olá ${row.Nome}, tudo bem?\n Sou o assistente Virtual do Salão Rudi Tomielo 🤖!\n`;
            mensagem += `\n🔈 Passando pra reforçar os seus horários no dia ${row.Data} (${row.Dia}) 🗓:\n`;

            // Separar os serviços, horários e profissionais em arrays
            const servicos = row['Serviço'].split(',');
            const horarios = row.Hora.split(',');
            const profissionais = row.Profissional.split(',');

            // Concatenar cada conjunto de serviço, horário e profissional em uma nova linha
            for (let i = 0; i < servicos.length; i++) {
                mensagem += `\n✅ *Serviço:* ${servicos[i]}\n🕥 *Horário:* ${horarios[i]}\n🪮 *Profissional:* ${profissionais[i]}\n\n`;
            }

            // Restante da mensagem
            mensagem += '\n⏳ Caso tenha algum motivo que não possa vir, solicito gentilmente que nos avise com no mínimo 24h de antecedência. ⏳\n';
            mensagem += '\nRessaltamos também que o não comparecimento no horário marcado implicará na cobrança de 50% do valor do serviço.\n';
            mensagem += '\nAgradecemos sua confiança e compreensão. 💌\n';

            // Número de telefone para enviar a mensagem
            const contactNumber = row.Telefone + '@c.us';

            // Enviar a mensagem
            client.sendMessage(contactNumber, mensagem)
                .then(() => console.log(`Mensagem enviada com sucesso para ${row.Cliente}`))
                .catch(err => console.error('Erro ao enviar mensagem:', err));
        })
        .on('end', () => {
            console.log('Leitura do arquivo CSV concluída.');
        });
});

// Inicializar o cliente
client.initialize();
