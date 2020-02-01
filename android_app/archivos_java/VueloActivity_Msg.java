package com.example.tfg;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;

import java.io.DataOutputStream;
import java.net.Socket;

public class VueloActivity_Msg extends AppCompatActivity {

    double[] latitudes;
    double[] longitudes;
    boolean vuelta;
    double altura;
    String ip;
    String port;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_vuelo__msg);

        Bundle ajustes = getIntent().getExtras();

        //leemos parametros enviados al iniciar la actividad
        ip = ajustes.getString("ip");
        port = ajustes.getString("port");
        vuelta = ajustes.getBoolean("vuleta");
        altura = ajustes.getDouble("altura");
        latitudes = ajustes.getDoubleArray("lat");
        longitudes = ajustes.getDoubleArray("lng");

        String msg = crearMSG(); //creamos mensaje que enviaremos por tcp

        //lanzamos clase que ejecuta el socket cliente y envia los datos
        backGroundTask b = new backGroundTask();
        b.execute(ip,port,msg);

    }

    public void btnSalir(View view){
        Intent intent = new Intent(this, MainActivity.class);
        startActivity(intent);
    }

    public String crearMSG (){
        /*
        * estructura: altura|lat,long|lat,long|lat,long
        * */
        String msg = "";
        msg = msg.concat(String.valueOf(altura));

        for(int i=0; i< latitudes.length; i++){
            msg = msg.concat("|");
            msg = msg.concat(String.valueOf(latitudes[i]));
            msg = msg.concat(",");
            msg = msg.concat(String.valueOf(longitudes[i]));
        }

        if(vuelta){
            msg = msg.concat("|");
            msg = msg.concat(String.valueOf(latitudes[0]));
            msg = msg.concat(",");
            msg = msg.concat(String.valueOf(longitudes[0]));
        }
        return msg;
    }

    class backGroundTask extends AsyncTask<String,Void,String> {

        Socket s;
        DataOutputStream dos;
        String ip, message;
        int port;

        @Override
        protected String doInBackground(String... params ){
            //leemos parametros pasados a la clase
            ip = params[0];
            port = Integer.parseInt(params[1]);
            message = params[2];

            try{
                Socket socket = s = new Socket(ip, port);//socket cliente
                dos = new DataOutputStream(s.getOutputStream());
                dos.writeUTF(message); //enviamos mensaje
                dos.close();//cerramos flujo
                s.close();//cerramos conexion
            }catch(Exception e){}
            return null;
        }


    }



}
