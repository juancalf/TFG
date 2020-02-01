package com.example.tfg;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.graphics.PointF;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.content.Intent;
import com.here.android.mpa.common.GeoCoordinate;
import com.here.android.mpa.common.Image;
import com.here.android.mpa.common.OnEngineInitListener;
import com.here.android.mpa.common.ViewObject;
import com.here.android.mpa.mapping.Map;
import com.here.android.mpa.mapping.MapFragment;
import com.here.android.mpa.mapping.MapGesture;
import com.here.android.mpa.mapping.MapMarker;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;


public class VueloActivity_Map extends AppCompatActivity implements LocationListener {

    //puntos seleccionados
    private List mapMakers;
    private List puntos;
    private List<Double> longitudes;
    private List<Double> latitudes;

    private Map map;
    private MapFragment mapFragment;
    private GeoCoordinate droneCord;//coordenadas del dron
    private LocationManager locationManager;//gestor de ubicacion

    //parametros de comunicacion y de vuelo
    boolean vuelta;
    double altura;
    String ip;
    String port;

    //ubicacion del dron en formato decimal
    double longitud;
    double latitud;


    @RequiresApi(api = Build.VERSION_CODES.M)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_vuelo_map);

        Bundle ajustes = getIntent().getExtras();

        ini();//inicializamos clase

        //leemos parametros
        ip  = ajustes.getString("ip");
        port = ajustes.getString("port");
        altura = ajustes.getDouble("altura");
        vuelta = ajustes.getBoolean("volverOrig");

        //gestor de localizaciones
        locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);

        //comprobamos que tenemos los permisos de localizacion activados
        if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED
                && checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            Log.e("errorUbicacion", "no se ha podido obtener la ubicacion");
            return;
        }

        //leemos la ultima ubicacion conocida
        Location location = locationManager.getLastKnownLocation(locationManager.NETWORK_PROVIDER);

        onLocationChanged(location);

        //creamos un mapa y establecemos la ubicacion del dron en el
        mapFragment = (MapFragment) getFragmentManager().findFragmentById(R.id.mapfragment);

        mapFragment.init(new OnEngineInitListener() {

            @Override
            public void onEngineInitializationCompleted(OnEngineInitListener.Error error) {
                if (error == OnEngineInitListener.Error.NONE) {

                    mapFragment.getMapGesture().addOnGestureListener(new MyOnGestureListener());

                    map = mapFragment.getMap();

                    setDroneCord();
                    map.setCenter(droneCord, Map.Animation.NONE);
                    map.setZoomLevel(map.getMaxZoomLevel(), Map.Animation.NONE);

                    setDroneMarker();
                }

                else
                    Log.e("errorMapa","error al iniciar los componentes del mapa");
            }
        });
    }

    @Override
    public void onLocationChanged(Location location) {
        //leemos los nuevos valores de la ubicacion
        longitud = location.getLongitude();
        latitud = location.getLatitude();
    }

    @Override
    public void onStatusChanged(String s, int i, Bundle bundle) {}

    @Override
    public void onProviderEnabled(String s) {}

    @Override
    public void onProviderDisabled(String s) {}

    //inicializamos las listas auxiliares
    private void ini(){
        mapMakers = new ArrayList();
        puntos = new ArrayList();
        longitudes = new ArrayList();
        latitudes = new ArrayList();
    }

    //establecemos las coordenadas leidas por la funcion onLocationChanged en el mapa
    private void setDroneCord(){
        droneCord = new GeoCoordinate(latitud, longitud);
    }

    private void setDroneMarker(){

        Image marker_img = new Image();//creamos un objeto imagen(sera la ubicacion del dron)

        try {
            marker_img.setImageAsset("drone.png");//establecemos una imagen
        } catch (IOException e) {
            e.printStackTrace();
        }

        //colocamos esa imagen en las coordenadas del objeto droneCord
        MapMarker m = new MapMarker().setCoordinate(droneCord);
        m.setIcon(marker_img);
        mapMakers.add(m);
        map.addMapObject(m);

    }

    private void actualizarMarker() {

        if (puntos.size() <= 10) { //limitamos el numero de puntos a un maximo de diez

            PointF point = (PointF) puntos.get(puntos.size() - 1);//leemos el punto seleccionado
            GeoCoordinate cord = map.pixelToGeo(point); //convertimos el punto a coordenadas

            latitudes.add(cord.getLatitude());//obtenemos latitud y longitud
            longitudes.add(cord.getLongitude());

            Image marker_img = new Image();

            //creamos una imagen con el numero de punto correcto
            try {
                String concat = puntos.size() + ".png";
                marker_img.setImageAsset(concat);
            } catch (IOException e) {
                e.printStackTrace();
            }

            //añadimos la imagen al mapa
            MapMarker m = new MapMarker().setCoordinate(cord);
            m.setIcon(marker_img);
            mapMakers.add(m);
            map.addMapObject(m);
        }
    }

    public void btnReset(View view){
        map.removeMapObjects(mapMakers); //borramos puntos del mapa
        ini(); //reinicializamos listas
        setDroneMarker(); //establecemos ubicacion
    }

    public void btnIniciar(View view){
        Intent intent = new Intent(this, VueloActivity_Msg.class);//nueva actividad

        double lats [] = new double [latitudes.size()];
        double lngs [] = new double [longitudes.size()];

        for(int i= 0; i<latitudes.size(); i++) { //convertimos las listas a arrays para poder pasarlas a la otra actividad
            lats[i] = latitudes.get(i);
            lngs[i]= longitudes.get(i);
        }

        //copiamos datos como parametros
        intent.putExtra("volverOrig", vuelta);
        intent.putExtra("altura", altura);
        intent.putExtra("ip", ip);
        intent.putExtra("port", port);
        intent.putExtra("lng",lngs);
        intent.putExtra("lat",lats);

        startActivity(intent);//comenzamos nueva actividad∫
    }

    //clase que se encarga de reconocer las pulsaciones en el mapa
    private class MyOnGestureListener implements MapGesture.OnGestureListener {

        @Override
        public boolean onTapEvent(PointF pointF) {//cuando pulsamos en el mapa...
            puntos.add(pointF); //se añade un nuevo punto a la lista
            actualizarMarker(); //llamamos a la funcion actualizar
            return true;
        }

        @Override
        public void onPanStart() {}

        @Override
        public void onPanEnd() {}

        @Override
        public void onMultiFingerManipulationStart() {}

        @Override
        public void onMultiFingerManipulationEnd() {}

        @Override
        public boolean onMapObjectsSelected(List<ViewObject> list) {
            return false;
        }

        @Override
        public boolean onDoubleTapEvent(PointF pointF) {
            return false;
        }

        @Override
        public void onPinchLocked() {}

        @Override
        public boolean onPinchZoomEvent(float v, PointF pointF) {
            return false;
        }

        @Override
        public void onRotateLocked() {}

        @Override
        public boolean onRotateEvent(float v) {
            return false;
        }

        @Override
        public boolean onTiltEvent(float v) {
            return false;
        }

        @Override
        public boolean onLongPressEvent(PointF pointF) {
            return false;
        }

        @Override
        public void onLongPressRelease() {}

        @Override
        public boolean onTwoFingerTapEvent(PointF pointF) {
            return false;
        }
    }

}