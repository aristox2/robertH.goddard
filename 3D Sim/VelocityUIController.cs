using UnityEngine;
using TMPro;

public class VelocityUIController : MonoBehaviour
{
    public RocketFlightController flightController;
    public TMP_Text velocityText;
    void Update()
    {
        if (flightController != null && velocityText != null)
        {
            float velocity = flightController.currentVelocity;
            velocityText.text = "Velocity: " + velocity.ToString("F1") + " m/s";
        }
    }
}