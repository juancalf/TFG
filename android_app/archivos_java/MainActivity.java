package com.example.tfg;

import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;


public class MainActivity extends AppCompatActivity {
    //parametros del protocolo de comunicacion y del dron
    private String ip;
    private String port;
    private double altura;
    private boolean volverOrig;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        getSupportActionBar().hide(); //oculta la barra de titulo para la vista principal
        Bundle ajustes = getIntent().getExtras();//si ha sido llamada desde ajustes implica que los ajustes predeterminados han cambiado
        if (ajustes == null) { //si son los ajustes predeterminados
            ip = "192.168.1.36";
            port = "12345";
            altura = 3;
            volverOrig = false;
        }
        else{ //si no lo son leemos los parametros pasados al iniciar la actividad y los guardamos
            ip = ajustes.getString("ip");
            port = ajustes.getString("port");
            altura = ajustes.getDouble("altura");
            volverOrig = ajustes.getBoolean("volverOrig");
        }
    }

    // pasa a la actividad donde seleccionas el recorrido
    public void btnInicioVuelo(View view){
        Intent intent = new Intent(this, VueloActivity_Map.class);
        //pasamos los parametros de comunicacion y vuelo
        intent.putExtra("ip", ip);
        intent.putExtra("port", port);
        intent.putExtra("altura", altura);
        intent.putExtra("volverOrig", volverOrig);
        startActivity(intent);
    }

    //muestra ajustes
    public void btnAjustes(View view){
        Intent intent = new Intent(this, AjustesActivity.class);
        startActivity(intent);
    }

    //muestra informacion
    public void btnInfo(View view){
        Intent intent = new Intent(this, InfoActivity.class);
        startActivity(intent);
    }

}
