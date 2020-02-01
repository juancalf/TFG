package com.example.tfg;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;
import java.io.IOException;
import java.io.InputStream;

public class InfoActivity extends AppCompatActivity {

    private static String nombreArchivo = "info.txt"; //archivo .txt donde esta la informacion que queremos cargar

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_info);

        try{
            this.setText();
        } catch (IOException e){
            Log.e("InfoActivity", "Archivo no encontrado");
        }

    }

    private void setText() throws IOException {
        TextView infoText = (TextView) findViewById(R.id.infoText);

        InputStream inputStream = getAssets().open(nombreArchivo); //abrimos el archivo de texto
        byte[] buffer = new byte[inputStream.available()];
        inputStream.read(buffer);
        infoText.setText(new String(buffer)); //convertimos a String los bytes leidos y los cargamos en el TextView
        inputStream.close(); //finalizamos cerrando el archivo
    }
}