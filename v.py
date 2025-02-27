from flask import Flask, request, jsonify

app = Flask(__name__)

# حالة الضوء وقيمة السلايدر
light_status = "off"
slider_value = 0

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Control Light and Slider</title>
      <style>
        body { font-family: Arial; text-align: center; margin: 50px; }
        button, input { margin: 10px; padding: 10px; font-size: 16px; }
      </style>
    </head>
    <body>
      <h1>Control Light and Slider</h1>
      <button id="turnOnBtn">Turn ON</button>
      <button id="turnOffBtn">Turn OFF</button>
      <input type="range" id="slider" min="0" max="255" value="0" />
      <span id="sliderValue">0</span>
  <script>
    const slider = document.getElementById("slider");
    const turnOnBtn = document.getElementById("turnOn");
    const turnOffBtn = document.getElementById("turnOff");

    async function sendCommand(light_status, slider_value) {
        try {
            const res = await fetch("/status", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ light_status, slider_value }),
            });

            const data = await res.json();

            // استبدال التنبيه بإظهار رسالة في مكان معين على الصفحة
            const messageDiv = document.getElementById("message");
            messageDiv.textContent = data.message || "Command sent!";
            messageDiv.style.color = "green";

        } catch (error) {
            console.error("Error:", error);

            // عرض رسالة خطأ
            const messageDiv = document.getElementById("message");
            messageDiv.textContent = "Error sending command!";
            messageDiv.style.color = "red";
        }
    }

    turnOnBtn.onclick = () => sendCommand("on", slider.value);
    turnOffBtn.onclick = () => sendCommand("off", slider.value);
</script>

    </body>
    </html>
    """

@app.route("/status", methods=["GET", "POST"])
def status():
    global light_status, slider_value
    if request.method == "POST":
        light_status = request.form.get("light_status", "off")
        slider_value = int(request.form.get("slider_value", 0))
        return jsonify({"message": "Data received successfully!"})
    elif request.method == "GET":
        return jsonify({"light": light_status, "slider": slider_value})
    else:
        return jsonify({"error": "Method not allowed"}), 405

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
