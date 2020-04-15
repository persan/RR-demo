with Ada.Numerics.Discrete_Random;
with Ada.Text_IO;
procedure Rr_Demo.Main is
   use Ada.Text_IO;
   package Rand_Positive is new Ada.Numerics.Discrete_Random (Positive);
   Generator : Rand_Positive.Generator;

   Error : exception;

   Bug : Boolean := False;

   procedure Make_Bug is
   begin
      Bug := True;
   end Make_Bug;

   procedure Do_Bug is
   begin
      Bug := True;
   end Do_Bug;
   F : File_Type;
begin
   Rand_Positive.Reset (Generator);
   Open (F, In_File, "dummy.txt");
   Close (F);
   for I in 1 .. 10 loop
      if Rand_Positive.Random (Generator) < (Positive'Last / 100) then
         if Rand_Positive.Random (Generator) < (Positive'Last / 2) then
            Make_Bug;
         else
            Do_Bug;
         end if;
      end if;
   end loop;

   if Bug then
      raise Error;
   end if;

end Rr_Demo.Main;
