module Main exposing (main)

import Browser
import Html exposing (Html, div, h3, input, label, option, p, select, strong, text)
import Html.Attributes exposing (class, for, id, placeholder, selected, step, type_, value)
import Html.Events exposing (onInput)
import String


type alias Model =
    { milesInput : String
    , kilometersInput : String
    , paceMileInput : String
    , paceKilometerInput : String
    , raceDistanceInput : String
    , raceUnit : Unit
    , raceTimeInput : String
    }


type Unit
    = Miles
    | Kilometers


type Msg
    = UpdateMiles String
    | UpdateKilometers String
    | UpdatePaceMile String
    | UpdatePaceKilometer String
    | UpdateRaceDistance String
    | UpdateRaceUnit String
    | UpdateRaceTime String


main : Program () Model Msg
main =
    Browser.sandbox
        { init = init
        , update = update
        , view = view
        }


init : Model
init =
    { milesInput = ""
    , kilometersInput = ""
    , paceMileInput = ""
    , paceKilometerInput = ""
    , raceDistanceInput = ""
    , raceUnit = Miles
    , raceTimeInput = ""
    }


update : Msg -> Model -> Model
update msg model =
    case msg of
        UpdateMiles value ->
            { model | milesInput = value }

        UpdateKilometers value ->
            { model | kilometersInput = value }

        UpdatePaceMile value ->
            { model | paceMileInput = value }

        UpdatePaceKilometer value ->
            { model | paceKilometerInput = value }

        UpdateRaceDistance value ->
            { model | raceDistanceInput = value }

        UpdateRaceUnit value ->
            { model | raceUnit = parseUnit value }

        UpdateRaceTime value ->
            { model | raceTimeInput = value }


parseUnit : String -> Unit
parseUnit unitString =
    if unitString == "kilometers" then
        Kilometers

    else
        Miles


milesToKilometers : Float -> Float
milesToKilometers miles =
    miles * 1.60934


kilometersToMiles : Float -> Float
kilometersToMiles kilometers =
    kilometers / 1.60934


pacePerMileToPerKilometer : Float -> Float
pacePerMileToPerKilometer secondsPerMile =
    secondsPerMile / 1.60934


pacePerKilometerToPerMile : Float -> Float
pacePerKilometerToPerMile secondsPerKilometer =
    secondsPerKilometer * 1.60934


parseTimeString : String -> Result String Int
parseTimeString input =
    let
        parts =
            String.split ":" (String.trim input)

        toPositiveInt segment =
            case String.toInt segment of
                Just value_ ->
                    if value_ >= 0 then
                        Ok value_

                    else
                        Err "Time values must be non-negative."

                Nothing ->
                    Err "Time must use numbers only."
    in
    case parts of
        [ mm, ss ] ->
            Result.map2
                (\minutes seconds ->
                    if seconds < 60 then
                        minutes * 60 + seconds

                    else
                        -1
                )
                (toPositiveInt mm)
                (toPositiveInt ss)
                |> Result.andThen
                    (\total ->
                        if total >= 0 then
                            Ok total

                        else
                            Err "Seconds must be less than 60."
                    )

        [ hh, mm, ss ] ->
            Result.map3
                (\hours minutes seconds ->
                    if minutes < 60 && seconds < 60 then
                        (hours * 3600) + (minutes * 60) + seconds

                    else
                        -1
                )
                (toPositiveInt hh)
                (toPositiveInt mm)
                (toPositiveInt ss)
                |> Result.andThen
                    (\total ->
                        if total >= 0 then
                            Ok total

                        else
                            Err "Minutes and seconds must be less than 60."
                    )

        _ ->
            Err "Use HH:MM:SS or MM:SS format."


calculatePaceFromDistance : Float -> Int -> Result String { perMile : Float, perKilometer : Float }
calculatePaceFromDistance distanceInMiles totalSeconds =
    if distanceInMiles <= 0 then
        Err "Distance must be greater than zero."

    else if totalSeconds <= 0 then
        Err "Total time must be greater than zero."

    else
        let
            perMile =
                toFloat totalSeconds / distanceInMiles
        in
        Ok
            { perMile = perMile
            , perKilometer = pacePerMileToPerKilometer perMile
            }


formatNumber : Float -> String
formatNumber number =
    String.fromFloat (toFloat (round (number * 100)) / 100)


formatPace : Float -> String
formatPace totalSeconds =
    let
        rounded =
            round totalSeconds

        minutes =
            rounded // 60

        seconds =
            modBy 60 rounded

        secondsString =
            if seconds < 10 then
                "0" ++ String.fromInt seconds

            else
                String.fromInt seconds
    in
    String.fromInt minutes ++ ":" ++ secondsString


parsePositiveFloat : String -> Result String Float
parsePositiveFloat raw =
    case String.toFloat (String.trim raw) of
        Just number ->
            if number > 0 then
                Ok number

            else
                Err "Enter a value greater than zero."

        Nothing ->
            Err "Enter a valid number."


viewConversion : String -> Result String String -> Html msg
viewConversion labelText conversionResult =
    case conversionResult of
        Ok output ->
            p [ class "mt-2 mb-0 text-success" ] [ strong [] [ text (labelText ++ " " ++ output) ] ]

        Err message ->
            p [ class "mt-2 mb-0 text-danger" ] [ text message ]


view : Model -> Html Msg
view model =
    let
        milesResult =
            parsePositiveFloat model.milesInput
                |> Result.map milesToKilometers
                |> Result.map (\km -> formatNumber km ++ " km")

        kilometersResult =
            parsePositiveFloat model.kilometersInput
                |> Result.map kilometersToMiles
                |> Result.map (\mi -> formatNumber mi ++ " mi")

        paceMileResult =
            parseTimeString model.paceMileInput
                |> Result.map toFloat
                |> Result.map pacePerMileToPerKilometer
                |> Result.map (\sec -> formatPace sec ++ " per km")

        paceKilometerResult =
            parseTimeString model.paceKilometerInput
                |> Result.map toFloat
                |> Result.map pacePerKilometerToPerMile
                |> Result.map (\sec -> formatPace sec ++ " per mile")

        racePaceResult =
            case ( parsePositiveFloat model.raceDistanceInput, parseTimeString model.raceTimeInput ) of
                ( Ok distanceValue, Ok totalSeconds ) ->
                    let
                        distanceInMiles =
                            case model.raceUnit of
                                Miles ->
                                    distanceValue

                                Kilometers ->
                                    kilometersToMiles distanceValue
                    in
                    calculatePaceFromDistance distanceInMiles totalSeconds

                ( Err distanceError, _ ) ->
                    Err distanceError

                ( _, Err timeError ) ->
                    Err timeError
    in
    div [ class "row g-4" ]
        [ div [ class "col-lg-6" ]
            [ div [ class "card border-0 bg-light h-100" ]
                [ div [ class "card-body" ]
                    [ h3 [ class "h5" ] [ text "Distance Conversions" ]
                    , label [ class "form-label mt-3", for "milesInput" ] [ text "Miles to kilometers" ]
                    , input [ id "milesInput", class "form-control", type_ "number", step "0.01", placeholder "Example: 5", value model.milesInput, onInput UpdateMiles ] []
                    , viewConversion "Result:" milesResult
                    , label [ class "form-label mt-4", for "kilometersInput" ] [ text "Kilometers to miles" ]
                    , input [ id "kilometersInput", class "form-control", type_ "number", step "0.01", placeholder "Example: 10", value model.kilometersInput, onInput UpdateKilometers ] []
                    , viewConversion "Result:" kilometersResult
                    ]
                ]
            ]
        , div [ class "col-lg-6" ]
            [ div [ class "card border-0 bg-light h-100" ]
                [ div [ class "card-body" ]
                    [ h3 [ class "h5" ] [ text "Pace Conversions" ]
                    , label [ class "form-label mt-3", for "paceMileInput" ] [ text "Pace per mile (MM:SS) to pace per kilometer" ]
                    , input [ id "paceMileInput", class "form-control", type_ "text", placeholder "Example: 08:30", value model.paceMileInput, onInput UpdatePaceMile ] []
                    , viewConversion "Result:" paceMileResult
                    , label [ class "form-label mt-4", for "paceKilometerInput" ] [ text "Pace per kilometer (MM:SS) to pace per mile" ]
                    , input [ id "paceKilometerInput", class "form-control", type_ "text", placeholder "Example: 05:00", value model.paceKilometerInput, onInput UpdatePaceKilometer ] []
                    , viewConversion "Result:" paceKilometerResult
                    ]
                ]
            ]
        , div [ class "col-12" ]
            [ div [ class "card border-0 bg-light" ]
                [ div [ class "card-body" ]
                    [ h3 [ class "h5" ] [ text "Race Pace Calculator" ]
                    , p [ class "text-muted" ] [ text "Enter a race distance and total time to calculate pace per mile and per kilometer." ]
                    , div [ class "row g-3" ]
                        [ div [ class "col-md-4" ]
                            [ label [ class "form-label", for "raceDistance" ] [ text "Distance" ]
                            , input [ id "raceDistance", class "form-control", type_ "number", step "0.01", placeholder "Example: 13.1", value model.raceDistanceInput, onInput UpdateRaceDistance ] []
                            ]
                        , div [ class "col-md-3" ]
                            [ label [ class "form-label", for "raceUnit" ] [ text "Unit" ]
                            , select [ id "raceUnit", class "form-select", onInput UpdateRaceUnit ]
                                [ option [ value "miles", selected (model.raceUnit == Miles) ] [ text "Miles" ]
                                , option [ value "kilometers", selected (model.raceUnit == Kilometers) ] [ text "Kilometers" ]
                                ]
                            ]
                        , div [ class "col-md-5" ]
                            [ label [ class "form-label", for "raceTime" ] [ text "Total time (HH:MM:SS or MM:SS)" ]
                            , input [ id "raceTime", class "form-control", type_ "text", placeholder "Example: 01:45:30", value model.raceTimeInput, onInput UpdateRaceTime ] []
                            ]
                        ]
                    , case racePaceResult of
                        Ok pace ->
                            div [ class "mt-3" ]
                                [ p [ class "mb-1 text-success" ] [ strong [] [ text ("Pace per mile: " ++ formatPace pace.perMile) ] ]
                                , p [ class "mb-0 text-success" ] [ strong [] [ text ("Pace per kilometer: " ++ formatPace pace.perKilometer) ] ]
                                ]

                        Err message ->
                            p [ class "mt-3 mb-0 text-danger" ] [ text message ]
                    ]
                ]
            ]
        ]