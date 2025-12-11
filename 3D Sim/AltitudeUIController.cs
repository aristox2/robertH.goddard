using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class AltitudeUIController : MonoBehaviour
{
    public Transform rocketTransform;
    //public Text altitudeTextl;
    public TMP_Text altitudeText;

    void Update()
    {
        if (rocketTransform != null && altitudeText != null)
        {
            // Update the text to show the current altitude
            float altitude = rocketTransform.position.y;
            altitudeText.text = "Altitude: " + altitude.ToString("F1") + " m";
        }
    }
}
