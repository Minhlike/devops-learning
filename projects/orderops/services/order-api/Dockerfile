# S14 checkpoint: build the jar with Maven before building this image.
# A tag is used deliberately; digest locking belongs to S17.
FROM eclipse-temurin:17-jre
WORKDIR /app
COPY target/order-api.jar app.jar
USER 10001
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
