using TMPro;
using UnityEngine;
using static UnityEditor.FilePathAttribute;

public class DriftUIController:MonoBehaviour
{
    public Transform rocketTransform;
    public TMP_Text locationText;

    void Update()
    {
        if (rocketTransform != null && locationText != null)
        {
            float xLocation = rocketTransform.position.y;
            locationText.text = "Drift(X): " + xLocation.ToString("F1") + " m/s";
        }
    }
}
