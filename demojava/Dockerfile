FROM maven:3.6.0-jdk-11-slim AS build
WORKDIR /app
COPY pom.xml ./
COPY ./src ./src
RUN mvn clean install


FROM openjdk:11-jre-slim
WORKDIR /app
EXPOSE 8080
COPY --from=build /app/target/*.jar /app/*.jar
ENTRYPOINT ["java", "-jar", "/app/*.jar" ]