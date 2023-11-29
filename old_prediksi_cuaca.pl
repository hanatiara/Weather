
% prediksi_cuaca.pl

% Define weather conditions
weather('Rain', [januari, februari, maret, april, oktober, november, december]).
weather('Clouds', [mei, juni, juli, agustus, september]).
weather('Hot', [juni, juli, agustus]).

% Rule for predicting weather
weather_prediction(City, Month, CurrentWeather) :-
    weather(CurrentWeather, Months),
    member(Month, Months),
    format('Prediksi cuaca di ~w pada bulan ~w adalah ~w.\n', [City, Month, CurrentWeather]).
