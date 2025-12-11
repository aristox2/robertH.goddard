using UnityEngine;

public class CameraFollow : MonoBehaviour
{
    private Quaternion initialRotation; // Stores the camera's starting rotation

    void Start()
    {
        // Record the initial rotation of the camera
        initialRotation = Quaternion.Euler(0, 0, 0);
        Debug.Log(initialRotation.eulerAngles.ToString());
    }

    void LateUpdate()
    {
        // Reset the camera's rotation to its initial rotation each frame
        transform.rotation = initialRotation;
    }
}
