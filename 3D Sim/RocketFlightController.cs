using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class RocketFlightController : MonoBehaviour
{
    [System.Serializable]
    public class FlightDataPoint
    {
        public float time;
        public float altitude;  // Zlocation is now altitude
        public float xLocation;
        public float pitch;
        public float velocity;  // Added velocity from CSV
    }

    public List<FlightDataPoint> flightDataPoints = new List<FlightDataPoint>();
    public Transform rocketTransform;

    public float currentVelocity { get; private set; }  // Expose velocity for UI

    void Start()
    {
        Application.targetFrameRate = 60;
        LoadCSV("filtered");
        StartCoroutine(SimulateFlight());
    }

    void LoadCSV(string fileName)
    {
        TextAsset csvFile = Resources.Load<TextAsset>(fileName);
        if (csvFile == null)
        {
            Debug.LogError("CSV file not found: " + fileName);
            return;
        }

        StringReader reader = new StringReader(csvFile.text);
        string line;
        bool isFirstLine = true;


        while ((line = reader.ReadLine()) != null)
        {
            if (isFirstLine)  // Skip header row
            {
                isFirstLine = false;
                continue;
            }

            string[] values = line.Split(',');
            if (values.Length >= 5)  // Ensure we have enough data
            {
                float time = float.Parse(values[0]);
                float altitude = float.Parse(values[2]);  // Zlocation now represents altitude
                float xLocation = float.Parse(values[1]);
                float pitch = float.Parse(values[3]);
                float velocity = float.Parse(values[4]);  // Read velocity from CSV

                flightDataPoints.Add(new FlightDataPoint
                {
                    time = time,
                    altitude = altitude,
                    xLocation = xLocation,
                    pitch = pitch,
                    velocity = velocity
                });
            }
        }

        Debug.Log("CSV file successfully loaded with " + flightDataPoints.Count + " data points.");
    }

    System.Collections.IEnumerator SimulateFlight()
    {
        if (flightDataPoints.Count == 0)
        {
            Debug.LogError("No flight data points available for simulation.");
            yield break;
        }

        for (int i = 0; i < flightDataPoints.Count - 1; i++)
        {
            if (rocketTransform == null)
            {
                Debug.LogError("rocketTransform is not assigned!");
                yield break;
            }

            FlightDataPoint currentPoint = flightDataPoints[i];
            FlightDataPoint nextPoint = flightDataPoints[i + 1];

            float timeElapsed = 0;
            float timeStep = 0.1f;  // Adjusted time step

            Vector3 startPosition = new Vector3(currentPoint.xLocation, currentPoint.altitude, rocketTransform.position.z);
            Vector3 endPosition = new Vector3(nextPoint.xLocation, nextPoint.altitude, rocketTransform.position.z);

            float startPitch = currentPoint.pitch;
            float endPitch = nextPoint.pitch;

            while (timeElapsed < timeStep)
            {
                rocketTransform.position = Vector3.Lerp(startPosition, endPosition, timeElapsed / timeStep);
                rocketTransform.rotation = Quaternion.Euler(0, 0, 90 - Mathf.Lerp(startPitch, endPitch, timeElapsed / timeStep));

                currentVelocity = Mathf.Lerp(currentPoint.velocity, nextPoint.velocity, timeElapsed / timeStep);  // Smooth velocity transition

                timeElapsed += Time.deltaTime;
                yield return null;
            }
        }
    }
}



