# Derived Fields

In an ideal world, our application logs have structured fields for the things we need to query by most of the time. On occasion, though, there is something that we want to query which is not a nice field.

I've learned that some systems for searching logs have _derived fields_ where we can use some transformation to compute a field for the purpose of our analysis. This field could be a simple boolean expression `fieldA contains "foo"` or some complex Regex to extract data from another field.

I'm documenting this for myself because I learned it recently at work, and it was quite valuable for an investigation.
