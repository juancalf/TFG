package com.example.tfg;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Switch;

public class AjustesActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_ajustes);
    }
      
    public void btnGuardar(View view){
        EditText ip = (EditText) findViewById(R.id.editText); //ip tcp
        EditText port = (EditText) findViewById(R.id.editText2); //puerto tcp
        EditText altura = (EditText) findViewById(R.id.editText3); //altura que llevara el dron
        Switch ret = (Switch) findViewById(R.id.switch1); //booleano de retorno al punto de partida

        Intent intent = new Intent(this, MainActivity.class); // al pulsar guardar vamos a saltar al menu(MainActivity)

        //guardamos como parametros para pasar a la nueva actividad los valores modificados de los ajustes
        intent.putExtra("ip", ip.getText().toString());
        intent.putExtra("port", port.getText().toString());
        intent.putExtra("altura", Double.parseDouble(altura.getText().toString()));
        intent.putExtra("volverOrig", ret.isChecked());

        startActivity(intent);//comenzamos nueva actividad
    }



}
