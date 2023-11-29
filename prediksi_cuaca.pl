% Facts about weather conditions
weather_condition(malang, mei, clouds, 21.28, 94, 0.49).
weather_condition(bandung, mei, clouds, 21.28, 94, 0.49).
weather_condition(jakarta, mei, clouds, 21.28, 94, 0.49).

% Rules for weather prediction
weather_prediction(City, Month, Weather, Temperature, Humidity, WindSpeed) :-
    weather_condition(City, Month, Weather, _, _, _),  % Ignore the existing values

    % Example conditions for weather prediction
    (Temperature > 25, Humidity < 50, WindSpeed < 1 ->
        write('Prediction: Clear Sky (Cerah)'), nl;
    Temperature > 20, Humidity < 80, WindSpeed < 2 ->
        write('Prediction: Partly Cloudy (Cerah Berawan)'), nl;
    Temperature > 15, Humidity > 70, WindSpeed < 3 ->
        write('Prediction: Rainy (Hujan)'), nl;
    % Add more conditions as needed
    write('Prediction: Uncertain')
    ).
